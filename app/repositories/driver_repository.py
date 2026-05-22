from sqlalchemy.orm import Session
from app.models.driver import Driver,FollowedDriver
from typing import Optional


class DriverRepository:
    def __init__(self,db:Session):
        self.db=db
    
    def get_all(self) ->list[Driver]:
        return self.db.query(Driver).all()
    
    def get_by_id(self,id:int) -> Optional[Driver]:
        return self.db.query(Driver).filter(Driver.id==id).first()
    
    def get_by_driver_id(self,driver_id:str)->Optional[Driver]:
        return self.db.query(Driver).filter(Driver.driver_id==driver_id).first()
    
    def create(self,driver_data:dict)->Driver:
        driver=Driver(**driver_data)
        self.db.add(driver)
        self.db.commit()
        self.db.refresh(driver)
        return driver
    
    def update(self,driver:Driver,driver_data:dict) -> Driver:
        for field, value in driver_data.items():
            setattr(driver,field,value)

        self.db.commit()
        self.db.refresh(driver)
        return driver
    
    def upsert(self,driver_data:dict) ->Driver:
        existing= self.get_by_driver_id(driver_data["driver_id"])
        if existing:
            return self.update(existing,driver_data)
        
        return self.create(driver_data)
    

    def get_followed_drivers(self,user_id:int,driver_id:int) ->list[FollowedDriver]:
        return self.db.query(FollowedDriver).filter(
            FollowedDriver.user_id==user_id
        ).all()
    

    def follow_driver(self,user_id:int,driver_id:int) -> FollowedDriver:
        followed=FollowedDriver(user_id=user_id,driver_ref_id=driver_id)
        self.db.add(followed)
        self.db.commit()
        self.db.refresh(followed)
        return followed
    
    def unfollow_driver(self,user_id:int,driver_id:int) -> bool:
        followed=self.db.query(FollowedDriver).filter(
            FollowedDriver.user_id==user_id,
            FollowedDriver.driver_ref_id==driver_id
        ).first()
        if not followed:
            return False
        self.db.delete(followed)
        self.db.commit()
        return True
    
    def is_following(self,user_id:int,driver_id:int) -> bool:
        return self.db.query(FollowedDriver).filter(
            FollowedDriver.user_id==user_id,
            FollowedDriver.driver_ref_id==driver_id
        ).first() is not None