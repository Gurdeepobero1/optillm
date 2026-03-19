from sqlalchemy import create_engine, Column, String, Float, Boolean, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid

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