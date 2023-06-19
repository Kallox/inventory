from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values(".env")

username = "postgres"
password = "7FgV77wBtmdIhS2dSUMl"
database = "railway"
ip = "containers-us-west-184.railway.app"
port = 5892

DATABASE_URL = f"postgresql://{username}:{password}@{ip}:{port}/{database}"
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#def get_session(): 
    #return Session
