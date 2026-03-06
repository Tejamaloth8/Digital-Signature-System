from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.db.models import User, Document, Signature
from app.core.security import hash_password, verify_password
from app.core.auth import get_current_user
from app.services.crypto_service import generate_keypair, sign_data, verify_signature
from app.services.file_crypto import generate_aes_key, encrypt_file, decrypt_file
import os, uuid, hashlib
from pydantic import BaseModel

router = APIRouter()
STORAGE_PATH = "storage"
os.makedirs(STORAGE_PATH, exist_ok=True)

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    password_hash = hash_password(data.password)
    private_key, public_key = generate_keypair()
    aes_key = generate_aes_key()

    user = User(
        email=data.email,
        password_hash=password_hash,
        private_key_enc=private_key,
        public_key=public_key,
        aes_key=aes_key
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    from app.services.crypto_service import create_access_token
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
