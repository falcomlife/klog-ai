from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Result(Base):
    __tablename__ = 'result'
    id = Column(String(40), primary_key=True)
    instance = Column(String(200))
    origin_index = Column(Text)
    auto_index = Column(Text)
    iforest_index = Column(Text)
    merge_index = Column(Text)
    time = Column(DateTime, default=datetime.now)
