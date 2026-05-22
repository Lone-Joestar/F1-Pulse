from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    #database
    database_url: str

    #JWT

    secret_key: str
    algorithm:str="HS256"
    access_token_expire_minutes:int=30
    refresh_token_expire_days:int=7


    #API
    app_name:str="F1 Pulse"
    app_version:str="1.0.0"
    debug:bool = True

    #Rate limiting
    free_tier_rate_limit:str="100/hour"
    premium_tier_rate_limit:str="1000/hour"

    #External APIs

    ergast_base_url: str="http://ergast.com/api/f1"

    class Config:
        env_file=".env"
        env_file_encoding="utf-8"
    
@lru_cache()
def get_settings() -> Settings:
        return Settings()