import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class EmailSummary(Base):
    __tablename__ = "email_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), unique=True, nullable=False)
    
    encrypted_summary = Column(Text, nullable=False) # Stores the encrypted JSON structure
    emails_analyzed = Column(Integer, default=0)
    
    last_refreshed = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("Client", back_populates="email_summary")
