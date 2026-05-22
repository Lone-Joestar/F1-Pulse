from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.driver_service import DriverService
from app.services.user_service import UserService
from app.config import get_settings
from slowapi import Limiter
from slowapi.util import get_remote_address

settings = get_settings()
limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/drivers", tags=["drivers"])

def get_driver_service(db: Session = Depends(get_db)) -> DriverService:
    return DriverService(db)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.get("/")
@limiter.limit(settings.free_tier_rate_limit)
async def get_all_drivers(
    request: Request,
    service: DriverService = Depends(get_driver_service)
):
    return await service.get_all_drivers()

@router.get("/standings")
@limiter.limit(settings.free_tier_rate_limit)
async def get_standings(
    request: Request,
    season: str = "current",
    service: DriverService = Depends(get_driver_service)
):
    return await service.get_standings(season)

@router.get("/{driver_id}")
@limiter.limit(settings.free_tier_rate_limit)
async def get_driver(
    request: Request,
    driver_id: str,
    service: DriverService = Depends(get_driver_service)
):
    return await service.get_driver(driver_id)

@router.post("/{driver_id}/follow")
async def follow_driver(
    driver_id: str,
    token: str,
    service: DriverService = Depends(get_driver_service),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_current_user(token)
    return await service.follow_driver(user, driver_id)

@router.delete("/{driver_id}/unfollow")
async def unfollow_driver(
    driver_id: str,
    token: str,
    service: DriverService = Depends(get_driver_service),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_current_user(token)
    return await service.unfollow_driver(user, driver_id)

@router.get("/me/following")
async def get_followed_drivers(
    token: str,
    service: DriverService = Depends(get_driver_service),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_current_user(token)
    return service.get_followed_drivers(user)