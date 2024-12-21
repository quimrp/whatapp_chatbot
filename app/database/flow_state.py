from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.database.models import Base

class FlowState(Base):
    __tablename__ = "flow_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, index=True)
    current_flow = Column(String)
    current_node = Column(String)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

