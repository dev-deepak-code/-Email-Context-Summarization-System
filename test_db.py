import asyncio
from app.db.database import AsyncSessionLocal
from sqlalchemy.future import select
from app.models.client import Client
from app.models.email import Email
from app.models.email_summary import EmailSummary
from app.services.encryption_service import encryption_service

async def main():
    async with AsyncSessionLocal() as session:
        clients = (await session.execute(select(Client))).scalars().all()
        print(f"Total Clients: {len(clients)}")
        for c in clients:
            print(f"Client: {c.id} - {c.name}")
            emails = (await session.execute(select(Email).where(Email.client_id == c.id))).scalars().all()
            print(f"  Emails count: {len(emails)}")
            summary = (await session.execute(select(EmailSummary).where(EmailSummary.client_id == c.id))).scalars().first()
            if summary:
                print(f"  Summary emails_analyzed: {summary.emails_analyzed}")
                print(f"  Summary decrypted: {encryption_service.decrypt(summary.encrypted_summary)}")
            else:
                print("  No summary found in DB")

asyncio.run(main())
