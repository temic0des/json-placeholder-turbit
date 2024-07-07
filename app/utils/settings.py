from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MongoDsn, ValidationInfo, field_validator

class Settings(BaseSettings):

    mongo_initdb_root_username: str
    mongo_initdb_root_password: str
    mongo_initdb_root_port: int
    mongo_initdb_root_host: str
    mongo_initdb_root_dbname: str
    mongo_url: Optional[MongoDsn] = None

    @field_validator('mongo_url', mode='before')
    @classmethod
    def build_mongo_url(cls, _: str, info: ValidationInfo):
        data = info.data
        return MongoDsn.build(scheme='mongodb',
                                    username=data.get('mongo_initdb_root_username'), 
                                   password=data.get('mongo_initdb_root_password'),
                                   host=data.get('mongo_initdb_root_host'),
                                   port=data.get('mongo_initdb_root_port'))

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding="utf-8")

settings = Settings()