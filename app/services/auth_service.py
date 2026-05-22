from datetime import datetime,timedelta
from typing import Optional
from jose import JWTError,jwt
import bcrypt
from app.config import get_settings
from app.schemas.user import TokenData


settings=get_settings()




def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



# creating access tokens

def create_access_token(data: dict)->str:
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire,"type":"access"})
    return jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)

#create refresh token

def create_refresh_token(data: dict) -> str:
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp":expire,"type":"refresh"})
    return jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)

# verifying tokens

def verify_token(token:str,token_type:str="access") -> Optional[TokenData]:
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        email:str=payload.get("sub")
        is_premium:bool=payload.get("is_premium",False)
        type_:str=payload.get("type")

        if email is None:
            return None
        if type_!=token_type:
            return None
        
        return TokenData(email=email,is_premium=is_premium)
    except JWTError:

        return None 
    

#creating both tokens


def create_tokens(email:str,is_premium:bool)-> dict:
    data={"sub":email,"is_premium":is_premium}
    return {
        "access_token":create_access_token(data),
        "refresh_token":create_refresh_token(data),
        "token_type":"bearer"
    }
