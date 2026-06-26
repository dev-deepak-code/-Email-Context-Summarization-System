class BaseAppException(Exception):
    """Base class for all custom application exceptions."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InvalidCredentialsException(BaseAppException):
    def __init__(self, message: str = "Invalid authentication credentials"):
        super().__init__(message=message, status_code=401)

class ItemNotFoundException(BaseAppException):
    def __init__(self, message: str = "Item not found"):
        super().__init__(message=message, status_code=404)

class ServiceUnavailableException(BaseAppException):
    def __init__(self, message: str = "External service is currently unavailable"):
        super().__init__(message=message, status_code=503)
