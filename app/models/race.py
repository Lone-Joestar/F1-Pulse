from sqlalchemy import Column , Integer, String, Float, ForeignKey, DateTime, JSON 
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Race(Base):
    __tablename__="races"

    id=Column(Integer,primary_key=True,index=True)
    season=Column(Integer,nullable=False,index=True)
    round=Column(Integer,nullable=False)
    race_name=Column(String(100),nullable=False)
    circuit_name=Column(String(100))
    circuit_id=Column(String(50))
    country=Column(String(50))
    locality=Column(String(50))
    date=Column(String(20))
    time=Column(String(20))

    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    results=relationship("RaceResult",back_populates="race")

    def __repr__(self):
        return f"<Race {self.season} Round {self.round} - {self.race_name}>"
    


class RaceResult(Base):
    __tablename__="race_results"

    id=Column(Integer,primary_key=True,index=True)
    race_id=Column(Integer,ForeignKey("races.id"),nullable=False)
    driver_id=Column(String(50),nullable=False)
    driver_name=Column(String(100))
    team=Column(String(100))
    position=Column(Integer)
    points=Column(Float)
    grid=Column(Integer)
    laps=Column(Integer)
    status=Column(String(50))
    fastest_lap_time=Column(String(20))
    fastest_lap_speed=Column(String(20))
    created_at=Column(DateTime,default=datetime.utcnow)
    race=relationship("Race",back_populates="results")

    def __repr__(self):
        return f"<RaceResult {self.driver_name} P{self.position}>"
    

class Constructor(Base):
    __tablename__="constructors"

    id=Column(Integer,primary_key=True,index=True)
    constructor_id=Column(String(50),unique=True,nullable=False,index=True)
    name=Column(String(100),nullable=False)
    nationality=Column(String(50))
    season=Column(Integer)
    position=Column(Integer)
    points=Column(Float)
    wins=Column(Integer)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Constructor {self.name}>"

