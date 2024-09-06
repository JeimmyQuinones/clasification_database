from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from api.application.config.config import settings

# Crear una instancia de MetaData
metadata = MetaData()

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()


def get_db_connection():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_db_connection_by_Url(urlConection: str):
    try:
        engineurl = create_engine(str(urlConection))
        dbUrl = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engineurl)
        )
        yield dbUrl
    finally:
        dbUrl.remove()
