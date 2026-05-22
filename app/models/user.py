from sqlalchemy import Column , Integer , String , Boolean ,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base 

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    email=Column(String(100),unique=True,nullable=False,index=True)
    hashed_password=Column(String(200),nullable=False)
    is_active=Column(Boolean,default=True)
    is_premium=Column(Boolean,default=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    followed_drivers=relationship("FollowedDriver",back_populates="user")
    webhooks=relationship("Webhook",back_populates="user")


    def __repr__(self):
        return f"<User {self.email}>"