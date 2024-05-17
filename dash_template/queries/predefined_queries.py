# Predefined SQL queries for each table
predefined_queries = {
    'banking': 'SELECT * FROM banking LIMIT 100',
    'mortgage': 'SELECT * FROM mortgage LIMIT 100',
    'sbl': 'SELECT * FROM sbl LIMIT 100'
}

def get_predefined_query(table_name):
    """
    Retrieve the predefined SQL query for a given table.

    Args:
        table_name (str): The name of the table.

    Returns:
        str: The predefined SQL query.
    """
    return predefined_queries.get(table_name, 'SELECT 1')
