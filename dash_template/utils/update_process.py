from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.banking import Banking
from models.mortgage import Mortgage
from models.sbl import Sbl
from config import DATABASE_URI

# Create a database engine
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def update_table(table_model, update_query, session):
    """
    Update the specified table using the provided SQL query.

    Args:
        table_model (Base): SQLAlchemy model representing the database table.
        update_query (str): SQL query string to update the table.
        session (Session): SQLAlchemy session object.
    """
    session.execute(text(update_query))
    session.commit()

def update_banking_table():
    """
    Update the banking table with new or updated data.
    """
    update_query = """
    INSERT INTO banking (id, name, balance)
    VALUES (1, 'John Doe', 1000.0), 
           (2, 'Jane Smith', 1500.0)
    ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    balance = EXCLUDED.balance;
    """
    update_table(Banking, update_query, session)

def update_mortgage_table():
    """
    Update the mortgage table with new or updated data.
    """
    update_query = """
    INSERT INTO mortgage (id, property_value, loan_amount)
    VALUES (1, 500000.0, 300000.0), 
           (2, 600000.0, 350000.0)
    ON CONFLICT (id) DO UPDATE SET
    property_value = EXCLUDED.property_value,
    loan_amount = EXCLUDED.loan_amount;
    """
    update_table(Mortgage, update_query, session)

def update_sbl_table():
    """
    Update the sbl table with new or updated data.
    """
    update_query = """
    INSERT INTO sbl (id, small_business_name, loan_amount)
    VALUES (1, 'Business A', 100000.0), 
           (2, 'Business B', 150000.0)
    ON CONFLICT (id) DO UPDATE SET
    small_business_name = EXCLUDED.small_business_name,
    loan_amount = EXCLUDED.loan_amount;
    """
    update_table(Sbl, update_query, session)

if __name__ == "__main__":
    # Update the tables with new data
    update_banking_table()
    update_mortgage_table()
    update_sbl_table()
