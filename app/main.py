from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.config import get_settings
from app.exceptions import F1PulseException

from app.database import engine, Base
import app.models

import structlog

settings=get_settings()

logger=structlog.get_logger()

Base.metadata.create_all(bind=engine)
app=FastAPI(
    title= settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

limiter=Limiter(key_func=get_remote_address)
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

origins=[
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(F1PulseException)
async def f1_pulse_exception_handler(request:Request,exc:F1PulseException):
    logger.error(
        "f1pulse_error",
        message=exc.message,
        status_code=exc.status_code,
        path=request.url.path
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error":exc.message}
    )


@app.get("/health")
async def health_check():
    return {
        "status":'healthy',
        "app":settings.app_name,
        "version":settings.app_version
    }


from app.routers.auth import router as auth_router
app.include_router(auth_router)

from app.routers.drivers import router as drivers_router
app.include_router(drivers_router)