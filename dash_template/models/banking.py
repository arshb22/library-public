from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Banking(Base):
    __tablename__ = 'banking'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Float)
