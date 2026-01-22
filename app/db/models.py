from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
from app.db.base import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String)
    topics = Column(JSON)
    sentiment = Column(String)
    materials_shared = Column(JSON)
    samples_distributed = Column(Integer)
    outcomes = Column(JSON)
    follow_ups = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
