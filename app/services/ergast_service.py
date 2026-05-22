import httpx
import asyncio
from typing import Optional
from app.config import get_settings
from app.exceptions import ExternalAPIException

settings=get_settings()

class ErgastService:
    def __init__(self):
        self.base_url=settings.ergast_base_url
        self.timeout=httpx.Timeout(10.0)

    #private get method
    async def _get(self,endpoint:str)->dict:
        url=f"{self.base_url}/{endpoint}.json"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response= await client.get(url)
                response.raise_for_status()
                return response.json()
            

        except httpx.TimeoutException:
            raise ExternalAPIException("Ergast",f"Timeot hitting {endpoint}")
        except httpx.HTTPStatusError as e:
            raise ExternalAPIException("Ergast",f"HTTP {e.response.status_code}")
        except Exception as e:
            raise ExternalAPIException("Ergast",str(e))


    #publc methids
    async def get_current_drivers(self) -> list:
        data=await self._get("current/drivers")
        drivers=data["MRData"]["DriverTable"]["Drivers"]
        return [self._parse_driver(d) for d in drivers]
    
    async def get_driver(self,driver_id:str) ->Optional[dict]:
        data=await self._get(f"drivers/{driver_id}")
        drivers=data["MRData"]["DriverTable"]["Drivers"]
        if not drivers:
            return None
        return self._parse_driver(drivers[0])
    
    async def get_driver_standings(self,season:str="current") -> list:
        data=await self._get(f"{season}/driverStandings")
        standings=data["MRData"]["StandingsTable"]["StandingsLists"]
        if not standings:
            return []
        return[self._parse_standing(s) for s in standings[0]["DriverStandings"]]
    

    async def get_race_calendar(self,season:str="current")-> list:
        data=await self._get(f"{season}")
        races=data["MRData"]["RaceTable"]["Races"]
        return [self._parse_race(r) for r in races]
    

    async def get_race_results(self,season:str,round:str)->dict:
        data=await self._get(f"{season}/{round}/results")
        races=data["MRData"]["RaceTable"]["Races"]
        if not races:
            return {}
        race=races[0]
        return{
            "race":self._parse_race(race),
            "results":[self._parse_result(r) for r in race.get("Results",[])]

        }

    async def get_constructor_standings(self,season:str="current")->list:
        data= await self._get(f"{season}/constructorStandings")
        standings=data["MRData"]["StandingsTable"]["StandingsLists"]
        if not standings:
            return []
        return [self._parse_constructor_standing(s) for s in standings[0]["ConstructorStandings"]]


    async def get_concurrent_season_data(self,season:str ="current") -> dict:
        drivers,calender,standings=await asyncio.gather(
            self.get_current_drivers(),
            self.get_race_calendar(season),
            self.get_driver_standings(season)
        )
        return {
            "drivers":drivers,
            "calender":calender,
            "standings":standings
        }

    def _parse_driver(self,d:dict) ->dict:
        return{
            "driver_id":d.get("driverId"),
            "name":f"{d.get('givenName')} {d.get('familyName')}",
            "nationality":d.get("nationality"),
            "date_of_birth":d.get("dateOfBirth"),
            "code":d.get("code"),
            "number":int(d.get("permanentNumber",0)) if d.get("permanentNumber") else None
        }   

    def _parse_standing(self,s:dict) ->dict:
        driver =s.get("Driver",{})
        constructor=s.get("Constructors",[{}])[0]
        return {
            "position":int(s.get("position",0)),
            "driver_id":driver.get("driverId"),
            "name":f"{driver.get('givenName')} {driver.get('familyName')}",
            "team":constructor.get("name"),
            "points":float(s.get("points",0)),
            "wins":int(s.get("wins",0))
        }

    def _parse_race(self,r:dict) -> dict:
        circuit=r.get("Circuit",{})
        location=circuit.get("Location",{})
        return{
            "season":int(r.get("season",0)),
            "round":int(r.get("round",0)),
            "race_name":r.get("raceName"),
            "circuit_name":circuit.get("circuitName"),
            "country":location.get("country"),
            "locality":location.get("locality"),
            "date":r.get("date"),
            "time":r.get("time")
        }

    def _parse_result(self,r:dict)->dict:
        driver=r.get("Driver",{})
        constructor=r.get("Constructor",{})
        fastest_lap=r.get("FastestLap",{})
        return{
            "driver_id":driver.get("driverId"),
            "driver_name":f"{driver.get("givenName")} {driver.get('familyName')}",
            "team":constructor.get("name"),
            "position":int(r.get("position",0)) if r.get("position") else None,
            "points":float(r.get("points",0)),
            "grid": int(r.get("grid",0)),
            "laps": int(r.get("laps",0)),
            "status":r.get("status"),
            "fastest_lap_time":fastest_lap.get("Time",{}).get("time"),
            "fastest_lap_speed":fastest_lap.get("AverageSpeed",{}).get("speed")        
        }
    
    def _parse_constructor_standing(self,s:dict) -> dict:
        constructor=s.get("Constructor",{})

        return {
            "constructor_id":constructor.get("constructorId"),
            "name":constructor.get("name"),
            "nationality":constructor.get("nationality"),
            "position":int(s.get('position',0)),
            "points":float(s.get("points",0)),
            "wins":int(s.get("wins",0))
        }