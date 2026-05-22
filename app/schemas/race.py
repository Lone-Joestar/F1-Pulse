from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List

class RaceBase(BaseModel):

    season:int
    round:int
    race_name: str
    circuit_name:Optional[str]=None
    circuit_id:Optional[str]=None
    country:Optional[str]=None
    locality:Optional[str]=None
    date: Optional[str]=None
    time: Optional[str]=None


class RaceCreate(RaceBase):
    pass 

class RaceResponse(RaceBase):
    id:int
    created_at:datetime
    updated_at:datetime

    class Config:
        from_attributes=True



class RaceResultBase(BaseModel):
    driver_id:str
    driver_name:Optional[str]=None
    team:Optional[int]=None
    position:Optional[int]=None
    points:Optional[float]=None
    grid:Optional[int]=None
    laps:Optional[int]=None
    status:Optional[str]=None
    fastest_lap_time:Optional[str]=None
    fastest_lap_speed:Optional[str]=None



class RaceResultCreate(RaceResultBase):
    race_id:int


class RaceResultResponse(RaceResultBase):
    id : int
    race_id : int
    created_at : datetime

    class Config:
        from_attributes=True


class RaceWithResults(RaceResponse):
    results: List[RaceResultResponse]=[]

    class Config:
        from_attributes=True


class ConstructorBase(BaseModel):
    constructor_id:str
    name: str
    nationality: Optional[str]=None
    season: Optional[int]=None
    position: Optional[int]=None
    points: Optional[float]=None
    wins: Optional[int]=None


class ConstructorCreate(ConstructorBase):
    pass 

class ConstructorResponse(ConstructorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True