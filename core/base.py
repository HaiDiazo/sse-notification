from pydantic import BaseSettings


class Settings(BaseSettings):
    BROKER_HOST: str
    BROKER_PASS: str
    BROKER_PORT: int
    BROKER_USER: str
    BROKER_VHOST: str

    BROKER_EXCHANGE: str
    BROKER_QUEUE: str
    BROKER_ROUTING: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
