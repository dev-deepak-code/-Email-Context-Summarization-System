import asyncio
import uuid
from datetime import datetime, timedelta
from app.db.database import AsyncSessionLocal
from app.models.firm import Firm
from app.models.accountant import Accountant, Role
from app.models.client import Client
from app.models.email import Email
from app.services.email_service import email_service

async def seed_data():
    async with AsyncSessionLocal() as session:
        # 1. Create a Firm
        firm = Firm(name="Smith & Associates CPA")
        session.add(firm)
        await session.flush()

        # 2. Create Accountants (Different Roles)
        from app.core.security import get_password_hash
        accountant = Accountant(
            firm_id=firm.id,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@smithcpa.com",
            password_hash=get_password_hash("securepassword123"),
            role=Role.ACCOUNTANT
        )
        firm_admin = Accountant(
            firm_id=firm.id,
            first_name="Admin",
            last_name="Smith",
            email="admin@smithcpa.com",
            password_hash=get_password_hash("securepassword123"),
            role=Role.FIRM_ADMIN
        )
        superuser = Accountant(
            firm_id=firm.id,
            first_name="Super",
            last_name="User",
            email="superuser@ascend.com",
            password_hash=get_password_hash("securepassword123"),
            role=Role.SUPERUSER
        )
        session.add_all([accountant, firm_admin, superuser])
        await session.flush()

        # 3. Create a Client
        client = Client(
            firm_id=firm.id,
            name="John Smith",
            email="john@example.com",
            company_name="TechCorp Inc."
        )
        session.add(client)
        await session.commit()
        await session.refresh(client)

        # 4. Create Mock Emails through the EmailService (so they get encrypted!)
        emails_data = [
            {
                "subject": "Missing W-2 forms",
                "body": "Hi John, I still need your W-2 for 2023. Please upload it to the portal ASAP. Thanks, Jane.",
                "sender_email": "jane.doe@smithcpa.com",
                "receiver_email": "john@example.com",
            },
            {
                "subject": "Re: Missing W-2 forms",
                "body": "Jane, I just uploaded it. Is there anything else you need? John.",
                "sender_email": "john@example.com",
                "receiver_email": "jane.doe@smithcpa.com",
            },
            {
                "subject": "1099 form pending",
                "body": "Thanks John. I have the W-2. We are still waiting on the 1099 from your brokerage account.",
                "sender_email": "jane.doe@smithcpa.com",
                "receiver_email": "john@example.com",
            }
        ]

        for i, data in enumerate(emails_data):
            e = Email(
                client_id=client.id,
                accountant_id=accountant.id,
                subject=data["subject"],
                body=data["body"],
                sender_email=data["sender_email"],
                receiver_email=data["receiver_email"],
                sent_at=datetime.utcnow() - timedelta(days=2 - i),
                message_id=str(uuid.uuid4())
            )
            # The service automatically encrypts the subject and body before calling the repository
            await email_service.create_email(e)

        print("\n" + "="*40)
        print("DATABASE SEEDED SUCCESSFULLY!")
        print("Use this Client ID to test the API:")
        print(f"👉 {client.id} 👈")
        print("="*40 + "\n")

if __name__ == "__main__":
    asyncio.run(seed_data())
