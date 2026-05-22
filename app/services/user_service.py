from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.services.auth_service import verify_password ,verify_token,create_tokens
from app.schemas.user import UserCreate,UserLogin,Token
from app.models.user import User
from app.exceptions import AlreadyExistsException, InvalidCredentialsException, UnauthorizedException


class UserService:
    def __init__(self,db:Session):

        self.repository=UserRepository(db)


    def register(self,user_data:UserCreate) ->User:

        existing=self.repository.get_by_email(user_data.email)
        if existing:
            raise AlreadyExistsException("User","email",user_data.email)
        return self.repository.create(user_data)
    

    def login(self,user_data:UserLogin)-> dict:
        user=self.repository.get_by_email(user_data.email)

        if not user:
            raise InvalidCredentialsException()
        
        if not verify_password(user_data.password,user.hashed_password):
            raise InvalidCredentialsException()
        if not user.is_active:
            raise UnauthorizedException("ACcount is deactivated")
        return create_tokens(user.email,user.is_premium)
    
    def refresh_token(self,token:str) -> dict:
        token_data=verify_token(token,token_type="refresh")
        if not token_data:
            raise UnauthorizedException("Invalyeid or expired refresh token")
        
        user=self.repository.get_by_email(token_data.email)

        if not user or not user.is_active:
            raise UnauthorizedException("User not found or deactivated")
        
        return create_tokens(user.email,user.is_premium)
    
    def get_current_user(self,token:str) -> User:
        token_data=verify_token(token)
        if not token_data:
            raise UnauthorizedException("Invalid or expired token")
        user=self.repository.get_by_email(token_data.email)

        if not user:
            raise UnauthorizedException("User not foubd")
        if not user.is_active:
            raise UnauthorizedException("account is deactivated")
        return user
    
    def get_premium_user(self,token:str) -> User:

        user=self.get_current_user(token)
        if not user.is_premium:
            raise UnauthorizedException("Premium subscription required")
        return user