import asyncio
import uuid
from datetime import datetime, timedelta
from app.db.database import AsyncSessionLocal
from app.models.client import Client
from app.models.email import Email
from app.models.firm import Firm
from app.models.accountant import Accountant
from sqlalchemy.future import select
from app.services.email_service import email_service

async def add_ram():
    async with AsyncSessionLocal() as session:
        # Grab the existing firm and accountant to attach the client to
        result = await session.execute(select(Firm).limit(1))
        firm = result.scalars().first()
        
        result = await session.execute(select(Accountant).limit(1))
        accountant = result.scalars().first()
        
        # 1. Create the new Client named "Ram"
        client = Client(
            firm_id=firm.id,
            name="Ram",
            email="ram@example.com",
            company_name="Ram Solutions"
        )
        session.add(client)
        await session.commit()
        await session.refresh(client)

        # 2. Add some brand new mock emails specifically for Ram
        emails_data = [
            {
                "subject": "Q3 Financial Reports",
                "body": "Hi Jane, I have attached the Q3 financial reports for Ram Solutions. Let me know if you need any further clarifications. Best, Ram.",
                "sender_email": "ram@example.com",
                "receiver_email": accountant.email,
            },
            {
                "subject": "Re: Q3 Financial Reports",
                "body": "Thanks Ram! Everything looks good, but I noticed missing invoices for August. Could you please send those over?",
                "sender_email": accountant.email,
                "receiver_email": "ram@example.com",
            },
            {
                "subject": "Re: Re: Q3 Financial Reports",
                "body": "Oops, my bad! I will get those August invoices over to you by tomorrow morning.",
                "sender_email": "ram@example.com",
                "receiver_email": accountant.email,
            }
        ]

        # 3. Save emails via EmailService (which will encrypt them and trigger OpenRouter in the background!)
        for i, data in enumerate(emails_data):
            e = Email(
                client_id=client.id,
                accountant_id=accountant.id,
                subject=data["subject"],
                body=data["body"],
                sender_email=data["sender_email"],
                receiver_email=data["receiver_email"],
                sent_at=datetime.utcnow() - timedelta(days=1 - i),
                message_id=str(uuid.uuid4())
            )
            await email_service.create_email(e)
            # Adding a tiny delay so the timestamps are staggered naturally
            await asyncio.sleep(0.5)

        print("\n" + "="*40)
        print("NEW CLIENT 'RAM' ADDED SUCCESSFULLY!")
        print(f"👉 NEW CLIENT ID: {client.id} 👈")
        print("="*40 + "\n")

if __name__ == "__main__":
    asyncio.run(add_ram())
