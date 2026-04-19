from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MechConnect FastAPI"
    API_V1_STR: str = ""
    SECRET_KEY: str = "supersecretkey_please_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # SQLite for development, change to postgres dynamically in production
    DATABASE_URL: str = "sqlite:///./mech_connect.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
