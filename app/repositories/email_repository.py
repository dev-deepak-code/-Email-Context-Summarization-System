from typing import List
from uuid import UUID
from sqlalchemy.future import select
from app.models.email import Email
from app.db.database import AsyncSessionLocal

class EmailRepository:
    """Handles basic CRUD operations for the Email model. Completely blind to encryption."""
    
    async def create(self, email: Email) -> Email:
        async with AsyncSessionLocal() as session:
            session.add(email)
            await session.commit()
            await session.refresh(email)
            return email

    async def get_by_client_id(self, client_id: UUID) -> List[Email]:
        async with AsyncSessionLocal() as session:
            stmt = select(Email).where(Email.client_id == client_id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

email_repository = EmailRepository()
