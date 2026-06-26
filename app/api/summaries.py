from fastapi import APIRouter, Depends, status
from uuid import UUID
from app.services.summary_service import summary_service
from app.schemas.response import CustomResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/summaries", tags=["Summaries"])

@router.get("/{client_id}", response_model=CustomResponse)
async def get_client_summary(client_id: UUID, current_user: dict = Depends(get_current_user)):
    """
    Get the structured email summary for a given client.
    Returns custom JSON response wrapping the data.
    """
    # OpenRouterError, EncryptionError and others are gracefully caught by main.py
    summary_data = await summary_service.get_or_generate_summary(client_id)
    
    return CustomResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Summary generated successfully.",
        data=summary_data
    )

@router.post("/{client_id}/refresh", response_model=CustomResponse)
async def refresh_client_summary(client_id: UUID, current_user: dict = Depends(get_current_user)):
    """
    Force refresh the summary for a given client.
    Follows flow: Auth -> Delete Cache -> Fetch Emails -> OpenRouter -> Encrypt -> Update DB -> Update Cache
    """
    # In a real app: Authenticate User via Depends()
    summary_data = await summary_service.refresh_summary(client_id)
    
    return CustomResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Summary refreshed successfully.",
        data=summary_data
    )
