from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.jwt import verify_access_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency that extracts the Bearer token from the Authorization header,
    verifies it, and returns the decoded payload. Raises 401 if invalid.
    """
    token = credentials.credentials
    payload = verify_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return payload

async def get_current_firm_admin(current_user: dict = Depends(get_current_user)) -> dict:
    role = current_user.get("role")
    if role not in ["FIRM_ADMIN", "SUPERUSER"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Requires Firm Admin privileges.",
        )
    return current_user

async def get_current_superuser(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") != "SUPERUSER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Requires Superuser privileges.",
        )
    return current_user
