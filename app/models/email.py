import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    accountant_id = Column(UUID(as_uuid=True), ForeignKey("accountants.id"), nullable=False)
    
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    
    sender_email = Column(String, nullable=False)
    receiver_email = Column(String, nullable=False)
    
    sent_at = Column(DateTime, nullable=False)
    message_id = Column(String, unique=True, nullable=False, index=True)

    client = relationship("Client", back_populates="emails")
    accountant = relationship("Accountant")
