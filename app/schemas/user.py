from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email:EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    email: str
    is_active:bool
    is_premium: bool
    created_at: datetime


    class Config:
        from_attributes=True
    

class UserUpdate(BaseModel):
    email: Optional[EmailStr]=None
    password: Optional[str]= None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type:str = "bearer"

class TokenData(BaseModel):
    email: Optional[str]=None
    is_premium: bool =False 