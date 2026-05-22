from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate,UserLogin,UserResponse,Token
from app.config import get_settings
from slowapi import Limiter
from slowapi.util import get_remote_address


settings=get_settings()
limiter=Limiter(key_func=get_remote_address)
router=APIRouter(prefix="/auth",tags=["auth"])

def get_user_service(db: Session =Depends(get_db)) -> UserService:
    return UserService(db)

@router.post("/register",response_model=UserResponse,status_code=201)
def register(
    user_data:UserCreate,
    service:UserService=Depends(get_user_service)
):
    return service.register(user_data)

@router.post("/login",response_model=Token)
@limiter.limit("5/minute")
def login(
    request:Request,
    user_data:UserLogin,
    service:UserService=Depends(get_user_service)
):
    return service.login(user_data)

@router.post("/refresh",response_model=Token)
def refresh(
    refresh_token:str,
    service:UserService=Depends(get_user_service)
):
    return service.refresh_token(refresh_token)

@router.get("/me",response_model=UserResponse)
def get_me(
    token:str,
    service:UserService=Depends(get_user_service)
):
    return service.get_current_user(token)