from pydantic import BaseSettings
from alembic import context


class Settings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_audience: str = "urn:dev"
    jwt_issuer: str = "urn:dev"
    jwt_leeway: float = 60
    handsy_database_url: str
    sql_echo: bool = False

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
