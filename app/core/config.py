from pydantic_settings import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):
  db_user: str = "postgres"
  db_password: str = ""
  db_host: str = "localhost"
  db_port: str = "5432"
  db_name: str = "cricket_db"
class Config:
  env_file = ".env"
  env_file_encoding = "utf-8"
@lru_cache()
def get_settings():
    return Settings()
