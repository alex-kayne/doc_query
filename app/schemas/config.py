from pydantic import BaseModel, model_validator


class AppSettings(BaseModel):
    name: str
    env: str
    host: str
    port: int


class DatabaseSettings(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str
    url: str | None = None
    sync_url: str | None = None

    @model_validator(mode='after')
    def compute_url(self):
        self.url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        self.sync_url = f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        return self


class RedisSettings(BaseModel):
    host: str
    port: int
    url: str | None = None

    @model_validator(mode='after')
    def compute_url(self):
        self.url = f"redis://{self.host}:{self.port}"
        return self


class LoggingSettings(BaseModel):
    level: str


class Settings(BaseModel):
    app: AppSettings
    database: DatabaseSettings
    redis: RedisSettings
    logging: LoggingSettings
