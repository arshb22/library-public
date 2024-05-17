import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.banking import Banking
from models.mortgage import Mortgage
from models.sbl import Sbl
from config import DATABASE_URI

# Create a database engine
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def load_csv_to_db(file_path, table_model, session):
    """
    Load data from a CSV file into the specified database table.

    Args:
        file_path (str): Path to the CSV file.
        table_model (Base): SQLAlchemy model representing the database table.
        session (Session): SQLAlchemy session object.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Convert DataFrame to list of dictionaries
    data = df.to_dict(orient='records')

    # Create a list of model instances
    records = [table_model(**record) for record in data]

    # Bulk insert the records into the database
    session.bulk_save_objects(records)
    session.commit()

def load_banking_data(file_path):
    load_csv_to_db(file_path, Banking, session)

def load_mortgage_data(file_path):
    load_csv_to_db(file_path, Mortgage, session)

def load_sbl_data(file_path):
    load_csv_to_db(file_path, Sbl, session)

if __name__ == "__main__":
    # Load data from CSV files into the database
    load_banking_data('data/banking.csv')
    load_mortgage_data('data/mortgage.csv')
    load_sbl_data('data/sbl.csv')
