# models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint

Base = declarative_base()

class ClickEvent(Base):
    __tablename__ = 'click_events'

    id = Column(Integer, primary_key=True)
    button_id = Column(String)
    timestamp = Column(DateTime, default=func.now())

class ClickCount(Base):
    __tablename__ = 'click_counts'

    id = Column(Integer, primary_key=True)
    button_id = Column(String)
    hour = Column(DateTime)
    count = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint('button_id', 'hour', name='_button_hour_uc'),)
