from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://avnadmin:AVNS_9qiRQNKHgF6nAThh1bn@pg-2692ca79-ayoubbomrane-bf7e.k.aivencloud.com:22294/wassalnimaak?sslmode=require'
engine =create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()