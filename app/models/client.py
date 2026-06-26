import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firm_id = Column(UUID(as_uuid=True), ForeignKey("firms.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    company_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    firm = relationship("Firm", back_populates="clients")
    emails = relationship("Email", back_populates="client", cascade="all, delete-orphan")
    email_summary = relationship("EmailSummary", back_populates="client", uselist=False, cascade="all, delete-orphan")
