from typing import Optional
from sqlalchemy.future import select
from app.models.accountant import Accountant
from app.db.database import AsyncSessionLocal

class AccountantRepository:
    """Repository for managing Accountant database operations."""
    
    async def get_by_email(self, email: str) -> Optional[Accountant]:
        async with AsyncSessionLocal() as session:
            stmt = select(Accountant).where(Accountant.email == email)
            result = await session.execute(stmt)
            return result.scalars().first()

accountant_repository = AccountantRepository()
