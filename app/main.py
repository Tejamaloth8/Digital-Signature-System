import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.api.auth import router as auth_router
from app.api.files import router as file_router

os.makedirs("storage", exist_ok=True)

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://digitalsignaturesystem.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Digital Signature System API is running"}

# Register routers
app.include_router(auth_router)
app.include_router(file_router)

# Create database tables
Base.metadata.create_all(bind=engine)