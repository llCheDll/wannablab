from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, String, Integer, Date, Text, Boolean
)

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)