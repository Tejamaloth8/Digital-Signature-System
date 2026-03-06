import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.api.auth import router as auth_router
from app.api.files import router as file_router

os.makedirs("storage", exist_ok=True)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Digital Signature System API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://digitalsignaturesystem.netlify.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False
)

app.include_router(auth_router)
app.include_router(file_router)

Base.metadata.create_all(bind=engine)