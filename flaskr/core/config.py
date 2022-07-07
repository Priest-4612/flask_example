from pathlib import Path

from dotenv import load_dotenv
from pydantic import AnyUrl, BaseSettings, PostgresDsn, validator

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR.joinpath('infra', 'env', '.env')
load_dotenv(dotenv_path=ENV_PATH)


class WSGISettings(BaseSettings):
    app: str = 'app.main:app'
    HOST: str = '0.0.0.0'
    PORT: int = 5005
    reload: bool = False
    workers: int = 3

    class Config:
        env_prefix = 'WSGI_'


class BaseDSNSettings(BaseSettings):
    USER: str = ''
    PASSWORD: str = ''
    HOST: str = ''
    PORT: int = 0
    PROTOCOL: str = ''
    PATH: str = ''
    DSN: AnyUrl = None

    @validator('DSN', pre=True)
    def build_dsn(cls, v, values) -> str:
        if v:
            return v

        protocol = values['PROTOCOL']
        user = values['USER']
        passwd = values['PASSWORD']
        host = values['HOST']
        port = values['PORT']
        path = values['PATH']

        if user and passwd:
            return '{protocol}://{user}:{passwd}@{host}:{port}/{path}'.format(
                protocol=protocol,
                user=user,
                passwd=passwd,
                host=host,
                port=port,
                path=path,
            )

        return '{protocol}://{host}:{port}/{path}'.format(
                protocol=protocol,
                host=host,
                port=port,
                path=path,
        )


class DatabaseSettings(BaseDSNSettings):
    PROTOCOL: str = 'postgresql'
    DSN: PostgresDsn = None
    SCHEMA: str = 'auth'

    class Config:
        env_prefix = 'POSTGRES_'


class CommonSettings(BaseSettings):
    FLASK_APP: str = 'app.main:app'
    DEBUG: bool = False
    WSGI: WSGISettings = WSGISettings()
    DB: DatabaseSettings = DatabaseSettings()
