from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    public_key = Column(LargeBinary, nullable=False)
    private_key_enc = Column(LargeBinary, nullable=False)
    aes_key = Column(LargeBinary, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    documents = relationship("Document", back_populates="owner")
    signatures = relationship("Signature", back_populates="signer")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="documents")
    signatures = relationship("Signature", back_populates="document")


class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    signer_id = Column(Integer, ForeignKey("users.id"))

    signature = Column(LargeBinary, nullable=False)
    heisenberg_r = Column(String, nullable=False)
    heisenberg_z = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="signatures")
    signer = relationship("User", back_populates="signatures")

    
class DocumentShare(Base):
    __tablename__ = "document_shares"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    shared_with_user_id = Column(Integer, ForeignKey("users.id"))