import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

if db_string := os.getenv("DB_STRING"):
    if "sqlite" in db_string:
        engine = create_engine(db_string, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(db_string)
else:  # Default to sqlite if there is no DB string supplied
    db_string = "sqlite:///./avatars_as_a_service/database/fun-avatars.sqlite.db"
    engine = create_engine(db_string, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# checkfirst option to make sure that tables are only created if they don't exist
async def init_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
