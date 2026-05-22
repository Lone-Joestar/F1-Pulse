from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import hash_password


class UserRepository:
    def __init__(self,db:Session):
        self.db=db
    

    def get_by_email(self,email:str)->User | None:
        return self.db.query(User).filter(User.email==email).first()
    
    def get_by_id(self,id:int) -> User | None:
        return self.db.query(User).filter(User.id==id).first()
    

    def create(self,user_data:UserCreate)->User:
        hashed=hash_password(user_data.password)
        user=User(
            email=user_data.email,
            hashed_password=hashed
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_premium(self,user:User,is_premium:bool)-> User:
        user.is_premium=is_premium
        self.db.commit()
        self.db.refresh(user)
        return user 
    

    def deactivate(self,user:User)-> User:
        user.is_active=False
        self.db.commit()
        self.db.refresh(user)
        return user 