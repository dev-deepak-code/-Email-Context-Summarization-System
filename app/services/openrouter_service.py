import httpx
import json
from typing import Dict, Any, List
from app.config import settings
from app.models.email import Email

class OpenRouterError(Exception):
    """Exception raised for OpenRouter API call failures."""
    pass

class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.OPENROUTER_MODEL

    async def generate_summary(self, emails: List[Email]) -> Dict[str, Any]:
        """
        Calls OpenRouter API to summarize a list of emails.
        Returns a structured dictionary containing 'actors', 'concluded_discussions', and 'open_action_items'.
        """
        if not self.api_key:
            raise OpenRouterError("OpenRouter API key is not configured.")

        # The EmailService will have decrypted these fields prior to calling this method
        email_text = "\n\n".join(
            f"From: {e.sender_email}\nTo: {e.receiver_email}\nSubject: {e.subject}\nBody: {e.body}"
            for e in emails
        )

        system_prompt = (
            "You are an assistant for a CPA firm. Your task is to analyze email threads "
            "between accountants and clients, and extract the context into a strictly structured JSON format. "
            "You MUST return ONLY valid JSON with exactly the following three keys:\n"
            "- 'actors': A list of strings of the names or roles of the people involved.\n"
            "- 'concluded_discussions': A list of strings describing topics that have been fully resolved.\n"
            "- 'open_action_items': A list of strings describing tasks that are pending or require action.\n\n"
            "Do not include any other text, markdown blocks, or explanation outside the JSON object."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze the following email thread:\n\n{email_text}"}
        ]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://email-context-system.local", 
            "X-Title": "Email Context System"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                
                content = data["choices"][0]["message"]["content"]
                
                # Parse the JSON string from the LLM response
                structured_data = json.loads(content)
                
                # Validate the required keys are present
                required_keys = {"actors", "concluded_discussions", "open_action_items"}
                if not required_keys.issubset(structured_data.keys()):
                    raise OpenRouterError("LLM response missing required JSON keys.")
                    
                return structured_data

        except httpx.TimeoutException:
            raise OpenRouterError("Request to OpenRouter timed out.")
        except httpx.HTTPStatusError as e:
            raise OpenRouterError(f"OpenRouter API returned HTTP status {e.response.status_code}")
        except json.JSONDecodeError:
            raise OpenRouterError("Failed to parse JSON response from LLM.")
        except Exception as e:
            if isinstance(e, OpenRouterError):
                raise e
            raise OpenRouterError(f"An unexpected error occurred during OpenRouter call: {str(e)}")

openrouter_service = OpenRouterService()
