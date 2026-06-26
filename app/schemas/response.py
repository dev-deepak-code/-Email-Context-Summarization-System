from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class CustomResponse(BaseModel, Generic[T]):
    success: bool
    status_code: int
    message: str
    data: Optional[T] = None
    error_details: Optional[Any] = None
