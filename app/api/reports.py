from fastapi import APIRouter, Depends, status
from app.api.deps import get_current_firm_admin, get_current_superuser
from app.repositories.summary_repository import summary_repository
from app.schemas.response import CustomResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/firm-summary", response_model=CustomResponse)
async def get_firm_summary_report(current_user: dict = Depends(get_current_firm_admin)):
    """
    Firm Admins: Can view a report of the total number of clients 
    with generated summaries within their firm.
    """
    firm_id = current_user.get("firm_id")
    count = await summary_repository.count_summaries_for_firm(firm_id)
    
    return CustomResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Firm summary report generated.",
        data={"total_clients_with_summaries": count, "firm_id": firm_id}
    )

@router.get("/global-summary", response_model=CustomResponse)
async def get_global_summary_report(current_user: dict = Depends(get_current_superuser)):
    """
    Superusers: Can view global reports (summaries generated across all firms, grouped by firm).
    """
    report_data = await summary_repository.get_global_summaries_grouped_by_firm()
    
    return CustomResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Global summary report generated.",
        data=report_data
    )
