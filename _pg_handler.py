import pandas as pd
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import insert

# Assume other necessary imports and .env loading are done above

# Your existing environment variable loading
hostname = os.getenv('POSTGRES_HOST')
db_name = os.getenv('DB_NAME')
schema = os.getenv('SCHEMA')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
endpoint_id = os.getenv('ENDPOINT_ID')

# Your existing function definitions

def check_sql_connection(hostname=hostname, db_name=db_name, username=username, password=password):
    try:
        # Create engine to connect to PostgreSQL database
        engine = create_engine(f'postgresql://{username}:{password}@{hostname}/{db_name}?options=endpoint%3D{endpoint_id}')
        # Connect to the database
        conn = engine.connect()
        # Close the connection
        conn.close()
        print("Database connection is successful.")
    except Exception as e:
        print(f"An error occurred: {e}")

def prep_df_for_table(df):
    return df

def generate_sql_schema(df, table_name):
    types_mapping = {
        'int64': Integer,
        'float64': Float,
        'object': String,
        'datetime64[ns]': DateTime
    }
    columns = [Column(col, types_mapping[str(df[col].dtype)]) for col in df.columns]
    return columns

def create_table(df, schema, table_name, hostname=hostname, user=username, password=password, db_name=db_name):
    # Create engine

    metadata = MetaData(schema=schema)
    # Assuming 'columns' are already defined by calling generate_sql_schema()
    columns = generate_sql_schema(df, table_name)  # You need to have df available here
    # Create Table object
    table = Table(table_name, metadata, *columns, schema=schema)
    # Create the table in the database
    table.create(engine, checkfirst=True)

def push_data_to_table(df, table_name, hostname=hostname, user=username, password=password, db_name=db_name):
    # Create engine
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{hostname}/{db_name}')
    # Prepare DataFrame for insert
    df = prep_df_for_table(df)
    # Insert data into table
    df.to_sql(table_name, engine, if_exists='append', index=False, schema=schema)

# Example usage
if __name__ == "__main__":
    print('run script')
    check_sql_connection()
    #push_data_to_table(df, 'example_table')
