from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sbl(Base):
    __tablename__ = 'sbl'
    id = Column(Integer, primary_key=True)
