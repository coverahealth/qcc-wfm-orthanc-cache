
from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlite_file: str
    log_level: str = "INFO"

    download_url: str
    upload_url: str
    find_endpoint:str
    username:str
    password:str
    instances_endpoint:str
    scheduler_frequency_min: int
    max_workers: int

    class Config:
        env_prefix = "QCC_WFM_CACHE_ORTHANC_"
        env_file = ".env"  # Environment variables will be loaded from this file
        

settings = Settings()