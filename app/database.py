from contextlib import contextmanager
from typing import final
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def provide_db_session(func):
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            return func(db, *args, **kwargs)
        finally:
            db.close()
    return wrapper