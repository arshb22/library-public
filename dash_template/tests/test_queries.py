import pytest
from queries.predefined_queries import get_predefined_query, predefined_queries
from queries.sql_generator import natural_language_to_sql, SQLQuery

def test_predefined_queries():
    banking_query = get_predefined_query('banking')
    assert banking_query == predefined_queries['banking']
    
    mortgage_query = get_predefined_query('mortgage')
    assert mortgage_query == predefined_queries['mortgage']
    
    sbl_query = get_predefined_query('sbl')
    assert sbl_query == predefined_queries['sbl']

    # Test for a non-existing table
    non_existing_query = get_predefined_query('non_existing_table')
    assert non_existing_query == 'SELECT 1'

def test_sql_query_generation():
    query = SQLQuery(dataset='banking', columns=['id', 'name', 'balance'], limit=50)
    generated_query = query.generate_query()
    expected_query = 'SELECT id, name, balance FROM banking LIMIT 50'
    assert generated_query == expected_query

    query = SQLQuery(dataset='mortgage', columns='*', limit=10)
    generated_query = query.generate_query()
    expected_query = 'SELECT * FROM mortgage LIMIT 10'
    assert generated_query == expected_query

def test_natural_language_to_sql(mocker):
    mocker.patch('queries.sql_generator.sql_chain.run', return_value='SELECT * FROM banking LIMIT 100')
    
    nl_query = 'Show me the first 100 entries from banking'
    sql_query = natural_language_to_sql(nl_query)
    
    expected_query = 'SELECT * FROM banking LIMIT 100'
    assert sql_query == expected_query
