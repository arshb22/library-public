import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.banking import Banking
from models.mortgage import Mortgage
from models.sbl import Sbl
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')  # Using an in-memory SQLite database for testing

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_banking_model(session):
    new_entry = Banking(id=1, name='John Doe', balance=1000.0)
    session.add(new_entry)
    session.commit()
    result = session.query(Banking).filter_by(id=1).first()
    assert result is not None
    assert result.name == 'John Doe'
    assert result.balance == 1000.0

def test_mortgage_model(session):
    new_entry = Mortgage(id=1, property_value=500000.0, loan_amount=300000.0)
    session.add(new_entry)
    session.commit()
    result = session.query(Mortgage).filter_by(id=1).first()
    assert result is not None
    assert result.property_value == 500000.0
    assert result.loan_amount == 300000.0

def test_sbl_model(session):
    new_entry = Sbl(id=1, small_business_name='Business A', loan_amount=100000.0)
    session.add(new_entry)
    session.commit()
    result = session.query(Sbl).filter_by(id=1).first()
    assert result is not None
    assert result.small_business_name == 'Business A'
    assert result.loan_amount == 100000.0
