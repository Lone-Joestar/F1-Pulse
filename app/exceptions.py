from fastapi import HTTPException,status

class F1PulseException(Exception):

    def __init__(self,message: str,status_code:int=500):
        self.message=message
        self.status_code=status_code
        super().__init__(message)

    
class NotFoundException(F1PulseException):

    def __init__(self,resource: str,id:int):
        super().__init__(
            message=f"{resource} with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class AlreadyExistsException(F1PulseException):
    def __init__(self,resource:str,field:str, value:str):
    
        super().__init__(
            message=f"{resource} with {field} '{value}' already exists",
            status_code=status.HTTP_400_BAD_REQUEST
        )


class UnauthorizedException(F1PulseException):
    def __init__(self,message:str="Not authorized"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class InvalidCredentialsException(F1PulseException):
    def __init__(self):
        super().__init__(
            message="invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class RateLimitException(F1PulseException):

    def __init__(self):
        super().__init__(
            message="Rate Limit exceeded",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
class ExternalAPIException(F1PulseException):
    def __init__(self,api_name:str,message:str):
        super().__init__(
            message=f"{api_name} API error: {message}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )