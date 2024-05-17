import pytest
import pandas as pd
from dash import Dash
from dash.testing.application_runners import import_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.banking import Banking
from models.mortgage import Mortgage
from models.sbl import Sbl
from queries.sql_generator import SQLQuery, natural_language_to_sql
from queries.predefined_queries import get_predefined_query
from config import DATABASE_URI

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')  # Use an in-memory SQLite database for testing

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

@pytest.fixture
def banking_data(session):
    data = [
        Banking(id=1, name='John Doe', balance=1000.0),
        Banking(id=2, name='Jane Smith', balance=1500.0),
        Banking(id=3, name='Alice Johnson', balance=2000.0)
    ]
    session.bulk_save_objects(data)
    session.commit()
    return data

@pytest.fixture
def mortgage_data(session):
    data = [
        Mortgage(id=1, property_value=500000.0, loan_amount=300000.0),
        Mortgage(id=2, property_value=600000.0, loan_amount=350000.0),
        Mortgage(id=3, property_value=550000.0, loan_amount=320000.0)
    ]
    session.bulk_save_objects(data)
    session.commit()
    return data

@pytest.fixture
def sbl_data(session):
    data = [
        Sbl(id=1, small_business_name='Business A', loan_amount=100000.0),
        Sbl(id=2, small_business_name='Business B', loan_amount=150000.0),
        Sbl(id=3, small_business_name='Business C', loan_amount=120000.0)
    ]
    session.bulk_save_objects(data)
    session.commit()
    return data

def test_sql_query_generation(session):
    query = SQLQuery(dataset='banking', columns=['id', 'name', 'balance'], limit=50)
    generated_query = query.generate_query()
    expected_query = 'SELECT id, name, balance FROM banking LIMIT 50'
    assert generated_query == expected_query

    result = session.execute(generated_query).fetchall()
    assert len(result) == 3

def test_natural_language_to_sql(mocker, session):
    mocker.patch('queries.sql_generator.sql_chain.run', return_value='SELECT * FROM banking LIMIT 100')
    
    nl_query = 'Show me the first 100 entries from banking'
    sql_query = natural_language_to_sql(nl_query)
    
    expected_query = 'SELECT * FROM banking LIMIT 100'
    assert sql_query == expected_query

    result = session.execute(sql_query).fetchall()
    assert len(result) == 3

def test_predefined_query_execution(session):
    query = get_predefined_query('banking')
    result = session.execute(query).fetchall()
    assert len(result) == 3

def test_dash_app(dash_duo, session, banking_data):
    app = import_app('app')
    
    dash_duo.start_server(app)

    # Input natural language query
    dash_duo.wait_for_element('#nl-query-input').send_keys('Show me the first 100 entries from banking')
    dash_duo.wait_for_element('#run-query-button').click()

    # Wait for graph to be updated and verify its content
    dash_duo.wait_for_element('#table-graph')
    assert dash_duo.get_logs() == [], "Browser console should contain no error"

    # Verify that summary statistics are displayed
    summary_stats = dash_duo.wait_for_element('#summary-stats').text
    assert 'Count' in summary_stats
    assert 'Mean' in summary_stats
    assert 'Std' in summary_stats

