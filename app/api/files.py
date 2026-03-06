from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import uuid
import hashlib
import tempfile

from app.db.deps import get_db
from app.db.models import User, Document, Signature, DocumentShare
from app.core.auth import get_current_user
from app.services.file_crypto import encrypt_file, decrypt_file
from app.services.crypto_service import sign_data, verify_signature
from app.services.heisenberg_service import (
    generate_keys,
    sign as h_sign,
    verify as h_verify,
    HeisenbergElement
)

router = APIRouter()

STORAGE_PATH = "storage"
os.makedirs(STORAGE_PATH, exist_ok=True)


# ------------------------
# Upload
# ------------------------
@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.email == user_email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")

        if not user.aes_key:
            raise HTTPException(status_code=500, detail="User AES key missing")

        raw_data = file.file.read()

        encrypted_data = encrypt_file(raw_data, user.aes_key)

        unique_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(STORAGE_PATH, unique_name)

        with open(file_path, "wb") as f:
            f.write(encrypted_data)

        document = Document(
            filename=file.filename,
            filepath=file_path,
            owner_id=user.id
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "message": "File uploaded successfully",
            "document_id": document.id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------
# Share Document
# ------------------------
@router.post("/share/{doc_id}")
def share_document(
    doc_id: int,
    recipient_email: str,
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    owner = db.query(User).filter(User.email == user_email).first()
    if not owner:
        raise HTTPException(status_code=401, detail="Invalid owner")

    recipient = db.query(User).filter(User.email == recipient_email).first()

    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.owner_id == owner.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found or not owned by you")

    share = DocumentShare(
        document_id=document.id,
        shared_with_user_id=recipient.id
    )

    db.add(share)
    db.commit()

    return {"message": f"Document shared with {recipient_email}"}


# ------------------------
# Download
# ------------------------
@router.get("/download/{doc_id}")
def download_file(
    doc_id: int,
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Check owner access
    if document.owner_id != user.id:

        shared = db.query(DocumentShare).filter(
            DocumentShare.document_id == doc_id,
            DocumentShare.shared_with_user_id == user.id
        ).first()

        if not shared:
            raise HTTPException(status_code=403, detail="Access denied")

    # Read encrypted file
    with open(document.filepath, "rb") as f:
        encrypted_data = f.read()

    # Always decrypt using OWNER AES key
    owner = db.query(User).filter(User.id == document.owner_id).first()

    decrypted_data = decrypt_file(encrypted_data, owner.aes_key)

    # Create temporary decrypted file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(document.filename)[1]) as temp_file:
        temp_file.write(decrypted_data)
        temp_path = temp_file.name

    return FileResponse(
        path=temp_path,
        filename=document.filename,
        media_type="application/octet-stream"
    )


# ------------------------
# Sign
# ------------------------
@router.post("/sign/{doc_id}")
def sign_document(
    doc_id: int,
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    with open(document.filepath, "rb") as f:
        encrypted_data = f.read()

    doc_hash = hashlib.sha256(encrypted_data).digest()

    ed_signature = sign_data(user.private_key_enc, doc_hash)

    g, h_private, h_public = generate_keys()
    r, z = h_sign(doc_hash, g, h_private)

    signature = Signature(
        document_id=document.id,
        signer_id=user.id,
        signature=ed_signature,
        heisenberg_r=f"{r.a},{r.b},{r.c}",
        heisenberg_z=str(z)
    )

    db.add(signature)
    db.commit()

    return {"message": "Document signed successfully"}


# ------------------------
# Verify
# ------------------------
@router.get("/verify/{doc_id}")
def verify_document(
    doc_id: int,
    db: Session = Depends(get_db)
):

    signature = (
        db.query(Signature)
        .filter(Signature.document_id == doc_id)
        .order_by(Signature.id.desc())
        .first()
    )

    if not signature:
        raise HTTPException(status_code=404, detail="No signature found")

    document = db.query(Document).filter(Document.id == doc_id).first()

    with open(document.filepath, "rb") as f:
        encrypted_data = f.read()

    doc_hash = hashlib.sha256(encrypted_data).digest()

    ed_valid = verify_signature(
        signature.signer.public_key,
        doc_hash,
        signature.signature
    )

    r = HeisenbergElement.deserialize(signature.heisenberg_r)
    z = int(signature.heisenberg_z)

    g, _, h_public = generate_keys()
    h_valid = h_verify(doc_hash, g, h_public, (r, z))

    return {
        "ed25519_valid": ed_valid,
        "heisenberg_valid": h_valid
    }