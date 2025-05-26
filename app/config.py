# This module defines application configuration using Pydantic's BaseSettings.
# It loads environment variables from a .env file and provides ccess
# to settings like database credentials. These settings can be accessed throughout
# the app via the `settings` instance.

from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str

    model_config = ConfigDict(env_file=".env")

settings = Settings()