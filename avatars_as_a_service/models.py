from datetime import datetime
from sqlalchemy import Integer, DateTime, Column, String, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base

from avatars_as_a_service.database.connection import Base


class Avatar(Base):
    __tablename__ = "avatar"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    image_hash = Column(String, nullable=False)
    image_url = Column(Text, nullable=False)
