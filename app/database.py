# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

Base = declarative_base()

engine1 = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
engine2 = create_engine(Config.SQLALCHEMY_DATABASE_URI_2, echo=True)

SessionLocal1 = sessionmaker(autocommit=False, autoflush=False, bind=engine1)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

def get_db1():
    db = SessionLocal1()
    try:
        yield db
    finally:
        db.close()

def get_db2():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()
