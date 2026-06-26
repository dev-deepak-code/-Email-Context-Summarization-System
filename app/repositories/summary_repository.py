from sqlalchemy.future import select
from sqlalchemy import func
from app.models.email_summary import EmailSummary
from app.models.client import Client
from app.models.firm import Firm
from app.db.database import AsyncSessionLocal

class SummaryRepository:
    """Handles basic CRUD operations for the EmailSummary model. Completely blind to encryption."""
    
    async def upsert(self, summary: EmailSummary):
        async with AsyncSessionLocal() as session:
            stmt = select(EmailSummary).where(EmailSummary.client_id == summary.client_id)
            result = await session.execute(stmt)
            existing = result.scalars().first()
            
            if existing:
                existing.encrypted_summary = summary.encrypted_summary
                existing.emails_analyzed = summary.emails_analyzed
                existing.last_refreshed = summary.last_refreshed
            else:
                session.add(summary)
                
            await session.commit()

    async def count_summaries_for_firm(self, firm_id: str) -> int:
        async with AsyncSessionLocal() as session:
            stmt = (
                select(func.count(EmailSummary.id))
                .join(Client, EmailSummary.client_id == Client.id)
                .where(Client.firm_id == firm_id)
            )
            result = await session.execute(stmt)
            return result.scalar() or 0

    async def get_global_summaries_grouped_by_firm(self):
        async with AsyncSessionLocal() as session:
            stmt = (
                select(Firm.id, Firm.name, func.count(EmailSummary.id).label("total_summaries"))
                .join(Client, Firm.id == Client.firm_id)
                .join(EmailSummary, Client.id == EmailSummary.client_id, isouter=True)
                .group_by(Firm.id, Firm.name)
            )
            result = await session.execute(stmt)
            return [{"firm_id": str(row.id), "firm_name": row.name, "total_summaries": row.total_summaries} for row in result]

summary_repository = SummaryRepository()
