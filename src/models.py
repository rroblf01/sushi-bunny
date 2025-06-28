import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

POSTGRES_USER = os.getenv("POSTGRES_USER", "sushi")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "sushi")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sushi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Table(Base):
    __tablename__ = "tables"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sushi_count = Column(Integer, default=0)
    table_id = Column(String, ForeignKey("tables.id"))
    table = relationship("Table", back_populates="users")


Table.users = relationship("User", back_populates="table")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
