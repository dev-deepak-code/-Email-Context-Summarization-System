from app.repositories.accountant_repository import accountant_repository
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

class AuthService:
    def __init__(self, repository=accountant_repository):
        self.repository = repository

    async def authenticate_user(self, login_data: LoginRequest) -> TokenResponse | None:
        """Verifies credentials and returns a JWT token if successful."""
        
        # 1. Fetch accountant by email
        accountant = await self.repository.get_by_email(login_data.email)
        if not accountant:
            return None
            
        # 2. Verify password securely using bcrypt
        if not verify_password(login_data.password, accountant.password_hash):
            return None
            
        # 3. Generate JWT Token containing useful standard claims
        token_data = {
            "sub": str(accountant.id),
            "role": accountant.role.value,
            "firm_id": str(accountant.firm_id)
        }
        access_token = create_access_token(data=token_data)
        
        return TokenResponse(access_token=access_token)

auth_service = AuthService()
