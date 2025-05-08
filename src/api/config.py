from functools import lru_cache
from pydantic import Field
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    _db_url: Optional[str] = Field(default=None, alias="DB_URL")
    db_type: str = Field(default="sqlite", alias="DB_TYPE")
    db_user: Optional[str] = Field(default=None, alias="DB_USER")
    db_password: Optional[str] = Field(default=None, alias="DB_PASSWORD")
    db_host: Optional[str] = Field(default=None, alias="DB_HOST")
    db_port: Optional[int] = Field(default=None, alias="DB_PORT")
    db_name: Optional[str] = Field(default=None, alias="DB_NAME")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Define the database url here
    @property
    def db_url(self):
        # If provide database variables
        if self.db_user and self.db_password and self.db_host and self.db_name:
            port_part = f":{self.db_port}" if self.db_port else ""

            if self.db_type == "mysql":
                return f"mysql+asyncmy://{self.db_user}:{self.db_password}@{self.db_host}{port_part}/{self.db_name}"

            # if self.db_type == "postgresql":
            #     return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}{port_part}/{self.db_name}"
        # If directly provide db_url
        elif self._db_url:
            return self._db_url
        # Database url is required
        else:
            raise ValueError("No valid database config found!")

    # Use relative url to located the .env at root
    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).parent.parent.parent}/.env"
    )


@lru_cache
def get_settings():
    return Settings()
