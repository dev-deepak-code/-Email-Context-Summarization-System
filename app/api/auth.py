from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.response import CustomResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=CustomResponse[TokenResponse])
async def login(login_data: LoginRequest):
    """
    Authenticate an accountant and return a JWT access token.
    """
    token = await auth_service.authenticate_user(login_data)
    
    if not token:
        # Standard generic 401 error so we don't leak whether an email exists or not
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return CustomResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Login successful.",
        data=token
    )
