import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.services.openrouter_service import OpenRouterError
from app.services.encryption_service import EncryptionError
from app.core.exceptions import BaseAppException
from app.api.summaries import router as summaries_router
from app.api.auth import router as auth_router
from app.api.reports import router as reports_router

app = FastAPI(title="Email Context & Summarization System")
logger = logging.getLogger(__name__)

# Include Routers
app.include_router(summaries_router)
app.include_router(auth_router)
app.include_router(reports_router)

@app.exception_handler(OpenRouterError)
async def openrouter_exception_handler(request: Request, exc: OpenRouterError):
    logger.error(f"OpenRouterError: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "success": False,
            "status_code": status.HTTP_502_BAD_GATEWAY,
            "message": "AI Summarization Service is currently unavailable or returned an error.",
            "error_details": None # Secure: don't leak API tokens or exact error traces
        }
    )

@app.exception_handler(EncryptionError)
async def encryption_exception_handler(request: Request, exc: EncryptionError):
    logger.error(f"EncryptionError: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "A security error occurred while processing sensitive data.",
            "error_details": None # Secure: don't leak key information
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        # Get the field name that caused the error
        field = error["loc"][-1] if len(error["loc"]) > 0 else "unknown"
        # Format a user-friendly message
        if error["type"] == "uuid_parsing":
            msg = f"Value must be a Guid."
        else:
            msg = error["msg"]
        errors.append(f"For '{field}': {msg}")
    
    error_message = "Please correct the following validation errors and try again. " + " ".join(errors)
    logger.error(f"Validation Error: {error_message}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": error_message,
            "error_details": exc.errors()
        }
    )

@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    logger.error(f"AppException ({exc.status_code}): {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.message,
            "error_details": None
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "An unexpected server error occurred.",
            "error_details": None
        }
    )
