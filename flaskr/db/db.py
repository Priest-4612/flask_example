from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from core.config import CommonSettings

settings = CommonSettings()

engine = create_engine(settings.DB.DSN, convert_unicode=True)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    ),
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import db.db_models  # noqa
    Base.metadata.create_all(bind=engine)

