from pydantic import Field
from pydantic_settings import BaseSettings

class DBConfig(BaseSettings):
    db_host: str = Field('127.0.0.1')
    db_port: int = Field(3306)

    class Config:
        env_file = ".env_ex"

print(DBConfig().model_dump())