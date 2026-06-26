import json
from datetime import datetime
from uuid import UUID
from typing import Dict, Any
from app.services.cache_service import cache_service
from app.services.encryption_service import encryption_service
from app.services.openrouter_service import openrouter_service
from app.services.email_service import email_service
from app.models.email_summary import EmailSummary

from app.repositories.summary_repository import summary_repository

class SummaryService:
    def __init__(self, repository=summary_repository):
        self.repository = repository

    async def get_or_generate_summary(self, client_id: UUID) -> Dict[str, Any]:
        """
        Retrieves the structured email summary for a client.
        Orchestrates Cache -> DB -> OpenRouter LLM.
        """
        str_client_id = str(client_id)

        # 1. Check cache for encrypted summary
        cached_encrypted = await cache_service.get_summary(str_client_id)
        if cached_encrypted:
            # Decrypt and parse JSON before returning via API
            decrypted_str = encryption_service.decrypt(cached_encrypted)
            return json.loads(decrypted_str)

        # 2. Fetch and decrypt emails using EmailService
        emails = await email_service.get_emails_for_client(client_id)
        if not emails:
            # Return empty structure if no emails exist
            return {"actors": [], "concluded_discussions": [], "open_action_items": []}

        # 3. Call OpenRouter to generate structured JSON
        structured_summary_dict = await openrouter_service.generate_summary(emails)

        # 4. Serialize JSON to string and Encrypt it
        summary_json_str = json.dumps(structured_summary_dict)
        encrypted_summary = encryption_service.encrypt(summary_json_str)

        # 5. Store in Database via Repository
        summary_record = EmailSummary(
            client_id=client_id,
            encrypted_summary=encrypted_summary,
            emails_analyzed=len(emails),
            last_refreshed=datetime.utcnow()
        )
        if self.repository:
            await self.repository.upsert(summary_record)

        # 6. Cache the *encrypted* summary string
        await cache_service.set_summary(str_client_id, encrypted_summary)

        # 7. Return the decrypted JSON dictionary directly to the API router
        return structured_summary_dict

    async def refresh_summary(self, client_id: UUID) -> Dict[str, Any]:
        """
        Forces a refresh of the summary exactly matching the required flow:
        Invalidate Cache -> Fetch Emails -> OpenRouter -> Encrypt -> DB -> Cache
        """
        str_client_id = str(client_id)
        
        # 1. Delete Existing Cache
        await cache_service.invalidate_summary(str_client_id)
        
        # 2. Call get_or_generate which will now hit a cache miss and execute the rest of the flow!
        return await self.get_or_generate_summary(client_id)

summary_service = SummaryService()
