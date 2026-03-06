from app.db.database import engine
from app.db.models import Base

def init():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

if __name__ == "__main__":
    init()
