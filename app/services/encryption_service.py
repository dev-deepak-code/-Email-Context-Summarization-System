from cryptography.fernet import Fernet, InvalidToken
from app.config import settings

class EncryptionError(Exception):
    """Exception raised for errors in the encryption process."""
    pass

class EncryptionService:
    def __init__(self):
        key = settings.ENCRYPTION_KEY
        if not key:
            raise ValueError("ENCRYPTION_KEY is not configured in the environment.")
        try:
            self.fernet = Fernet(key.encode())
        except Exception as e:
            raise ValueError(f"Invalid ENCRYPTION_KEY format: {str(e)}")

    def encrypt(self, data: str) -> str:
        """Encrypts a plaintext string using AES-256 (Fernet)."""
        if not data:
            return data
        try:
            return self.fernet.encrypt(data.encode()).decode()
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {str(e)}")

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypts a previously encrypted string."""
        if not encrypted_data:
            return encrypted_data
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except InvalidToken:
            raise EncryptionError("Invalid token: Decryption failed. The data might be corrupted or the key is incorrect.")
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {str(e)}")

encryption_service = EncryptionService()
