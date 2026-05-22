from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DriverBase(BaseModel):
    driver_id:str
    name: str
    nationality: Optional[str]=None
    team: Optional[str]=None
    number: Optional[str]=None
    code: Optional[str]=None
    date_of_birth: Optional[str]=None


class DriverCreate(DriverBase):
    pass

class DriverResponse(DriverBase):
    id:int
    created_at:datetime
    updated_at:datetime

    class Config:
        from_attributes=True
    

class DriverStanding(BaseModel):
    position:int
    driver_id:str
    name:str
    nationality:Optional[str]=None
    team:Optional[str]=None
    points: float
    wins: int
    
    class Config:
        from_attributes=True


class FollowedDriverResponse(BaseModel):
    id:int
    driver_id:int
    followed_at:datetime
    driver: DriverResponse

    class Config:
        from_attributes=True