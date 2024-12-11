from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in .env file")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(255), index=True)
    content = Column(String(1000))
    timestamp = Column(DateTime, default=datetime.utcnow)

class FlowState(Base):
    __tablename__ = "flow_states"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, index=True)
    current_flow = Column(String(255))
    current_node = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    logger.info("Inicializando la base de datos...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada con éxito")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise

if __name__ == "__main__":
    init_db()
