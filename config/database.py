from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values(".env")

username = config['USERNAME']
password = config['PASSWORD']
database = config['DATABASE']
ip = config['IP']
port = config['PORT']

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
