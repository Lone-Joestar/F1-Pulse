from sqlalchemy import Column , Integer, String,Float, ForeignKey, DateTime

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base

class Driver(Base):
    __tablename__="drivers"

    id=Column(Integer,primary_key=True,index=True)
    driver_id=Column(String(50),unique=True,nullable=False,index=True)
    name=Column(String(100),nullable=False)
    nationality=Column(String(50))
    team=Column(String(100))
    number=Column(Integer)
    code=Column(String(10))
    date_of_birth=Column(String(20))
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)


    followed_by=relationship("FollowedDriver",back_populates="driver")

    def __repr__(self):
        return f"<Driver {self.name}>"
    
class FollowedDriver(Base):

    __tablename__="followed_drivers"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    driver_ref_id=Column(Integer,ForeignKey("drivers.id"),nullable=False)
    followed_at=Column(DateTime,default=datetime.utcnow)

    user=relationship("User",back_populates="followed_drivers")
    driver=relationship("Driver",back_populates="followed_by")

    def __repr__(self):
        return f"<FollowedDriver user={self.user_id} driver={self.driver_ref_id}>"