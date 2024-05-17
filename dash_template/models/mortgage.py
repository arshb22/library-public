from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mortgage(Base):
    __tablename__ = 'mortgage'
    id = Column(Integer, primary_key=True)