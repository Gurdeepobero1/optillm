from sqlalchemy import create_engine, Column, String, Float, Boolean, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid
from sqlalchemy import create_engine, Column, String, Float, Boolean, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid

engine = create_engine("sqlite:///optillm.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    api_key = Column(String)

class Usage(Base):
    __tablename__ = "usage"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    query = Column(String)
    latency = Column(Float)
    cost = Column(Float)
    cached = Column(Boolean)

def init_db():
    Base.metadata.create_all(engine)

from streamlit import user

engine = create_engine("sqlite:///optillm.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    api_key = Column(String, unique=True)
    name = Column(String)

class Usage(Base):
    __tablename__ = "usage"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    query = Column(String)
    latency = Column(Float)
    cost = Column(Float)
    cached = Column(Boolean)

def init_db():
    Base.metadata.create_all(engine)
    def create_user(name, api_key):
        db = SessionLocal()
        user = User(name=name, api_key=api_key)
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
    return user

def get_user_by_name(name):
    db = SessionLocal()
    user = db.query(User).filter(User.name == name).first()
    db.close()
    return user

def update_api_key(user_id, new_key):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.api_key = new_key
        db.commit()
    db.close()

def create_user(name, api_key):
    db = SessionLocal()
    user = User(name=name, api_key=api_key)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def get_user_by_name(name):
    db = SessionLocal()
    user = db.query(User).filter(User.name == name).first()
    db.close()
    return user


def update_api_key(user_id, new_key):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.api_key = new_key
        db.commit()
    db.close()