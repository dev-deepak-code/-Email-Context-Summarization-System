from typing import List
from uuid import UUID
from app.models.email import Email
from app.services.encryption_service import encryption_service

from app.repositories.email_repository import email_repository

class EmailService:
    """
    Service handling Email business logic.
    """
    def __init__(self, repository=email_repository):
        self.repository = repository

    def encrypt_email(self, email: Email) -> Email:
        """Encrypts subject and body before saving."""
        if email.subject:
            email.subject = encryption_service.encrypt(email.subject)
        if email.body:
            email.body = encryption_service.encrypt(email.body)
        return email

    def decrypt_email(self, email: Email) -> Email:
        """Decrypts subject and body after retrieving."""
        if email.subject:
            email.subject = encryption_service.decrypt(email.subject)
        if email.body:
            email.body = encryption_service.decrypt(email.body)
        return email

    async def create_email(self, email: Email) -> Email:
        """
        Encrypts the email, saves it, and automatically triggers an asynchronous 
        background update of the AI summary.
        """
        if not self.repository:
            raise ValueError("Repository not injected")
            
        encrypted_email = self.encrypt_email(email)
        saved_email = await self.repository.create(encrypted_email)
        
        # Auto-trigger the summary refresh in the background!
        import asyncio
        from app.services.summary_service import summary_service
        asyncio.create_task(summary_service.refresh_summary(saved_email.client_id))
        
        return saved_email

    async def get_emails_for_client(self, client_id: UUID) -> List[Email]:
        """
        Retrieves emails for a client and immediately decrypts them before 
        returning them to the caller.
        """
        if not self.repository:
            raise ValueError("Repository not injected")
            
        encrypted_emails = await self.repository.get_by_client_id(client_id)
        return [self.decrypt_email(e) for e in encrypted_emails]

email_service = EmailService()
