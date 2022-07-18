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
    DATABASE_NAME: str = ''
    PROTOCOL: str = ''
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
        database_name = values['DATABASE_NAME']

        if user and passwd:
            return '{protocol}://{user}:{passwd}@{host}:{port}/{database_name}'.format(
                protocol=protocol,
                user=user,
                passwd=passwd,
                host=host,
                port=port,
                database_name=database_name,
            )

        return '{protocol}://{host}:{port}/{database_name}'.format(
                protocol=protocol,
                host=host,
                port=port,
                database_name=database_name,
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


if __name__ == '__main__':
    cfg = CommonSettings()
    print(cfg.DB)
