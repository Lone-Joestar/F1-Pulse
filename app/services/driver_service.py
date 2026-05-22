from sqlalchemy.orm import Session
from app.repositories.driver_repository import DriverRepository
from app.services.ergast_service import ErgastService
from app.schemas.driver import DriverResponse
from app.exceptions import NotFoundException
from app.models.user import User

class DriverService:
    def __init__(self, db: Session):
        self.repository = DriverRepository(db)
        self.ergast = ErgastService()

    async def sync_current_drivers(self) -> list:
        drivers = await self.ergast.get_current_drivers()
        return [self.repository.upsert(d) for d in drivers]

    async def get_all_drivers(self) -> list:
        drivers = self.repository.get_all()
        if not drivers:
            drivers = await self.sync_current_drivers()
        return [
        {
            "id": d.id,
            "driver_id": d.driver_id,
            "name": d.name,
            "nationality": d.nationality,
            "team": d.team,
            "number": d.number,
            "code": d.code,
            "date_of_birth": d.date_of_birth,
            "created_at": str(d.created_at),
            "updated_at": str(d.updated_at)
        }
        for d in drivers
    ]

    async def get_driver(self, driver_id: str) -> dict:
        driver = self.repository.get_by_driver_id(driver_id)
        if not driver:
            ergast_driver = await self.ergast.get_driver(driver_id)
            if not ergast_driver:
                raise NotFoundException("Driver", 0)
            driver = self.repository.upsert(ergast_driver)
        return driver

    async def get_standings(self, season: str = "current") -> list:
        return await self.ergast.get_driver_standings(season)

    async def follow_driver(self, user: User, driver_id: str) -> dict:
        driver = await self.get_driver(driver_id)
        already_following = self.repository.is_following(user.id, driver.id)
        if already_following:
            return {"message": f"Already following {driver.name}"}
        self.repository.follow_driver(user.id, driver.id)
        return {"message": f"Now following {driver.name}"}

    async def unfollow_driver(self, user: User, driver_id: str) -> dict:
        driver = self.repository.get_by_driver_id(driver_id)
        if not driver:
            raise NotFoundException("Driver", 0)
        unfollowed = self.repository.unfollow_driver(user.id, driver.id)
        if not unfollowed:
            return {"message": f"You were not following {driver.name}"}
        return {"message": f"Unfollowed {driver.name}"}

    def get_followed_drivers(self, user: User) -> list:
        return self.repository.get_followed_drivers(user.id)