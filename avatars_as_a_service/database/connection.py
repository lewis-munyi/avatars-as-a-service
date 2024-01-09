from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLITE_DB_PATH = "sqlite:///./avatars_as_a_service/database/aaas.sqlite.db"

engine = create_engine(
    SQLITE_DB_PATH, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def init_db():  # checkfirst option to make sure that tables are only created if they don't exist
    print("creating tables ")
    Base.metadata.create_all(bind=engine, checkfirst=True)


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
