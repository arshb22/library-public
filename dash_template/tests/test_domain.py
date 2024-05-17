import pytest
import pandas as pd
from domain.banking_domain import BankingDomain
from domain.mortgage_domain import MortgageDomain
from domain.sbl_domain import SblDomain

@pytest.fixture
def banking_data():
    data = {
        'id': [1, 2, 3],
        'name': ['John Doe', 'Jane Smith', 'Alice Johnson'],
        'balance': [1000.0, 1500.0, 2000.0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def mortgage_data():
    data = {
        'id': [1, 2, 3],
        'property_value': [500000.0, 600000.0, 550000.0],
        'loan_amount': [300000.0, 350000.0, 320000.0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sbl_data():
    data = {
        'id': [1, 2, 3],
        'small_business_name': ['Business A', 'Business B', 'Business C'],
        'loan_amount': [100000.0, 150000.0, 120000.0]
    }
    return pd.DataFrame(data)

def test_banking_domain_visualization(banking_data):
    domain = BankingDomain(banking_data)
    # Assuming visualize_balance_distribution method returns the figure object for testing
    fig = domain.visualize_balance_distribution()
    assert fig is not None
    assert 'data' in fig
    assert 'layout' in fig

def test_banking_domain_summary_statistics(banking_data):
    domain = BankingDomain(banking_data)
    summary = banking_data['balance'].describe().to_dict()
    assert 'count' in summary
    assert summary['count'] == 3
    assert summary['mean'] == 1500.0
    assert summary['std'] == 500.0

def test_mortgage_domain_visualization(mortgage_data):
    domain = MortgageDomain(mortgage_data)
    # Assuming visualize_loan_amount method returns the figure object for testing
    fig = domain.visualize_loan_amount()
    assert fig is not None
    assert 'data' in fig
    assert 'layout' in fig

def test_mortgage_domain_summary_statistics(mortgage_data):
    domain = MortgageDomain(mortgage_data)
    summary = mortgage_data['loan_amount'].describe().to_dict()
    assert 'count' in summary
    assert summary['count'] == 3
    assert summary['mean'] == 323333.3333333333

def test_sbl_domain_visualization(sbl_data):
    domain = SblDomain(sbl_data)
    # Assuming visualize_loan_amount method returns the figure object for testing
    fig = domain.visualize_loan_amount()
    assert fig is not None
    assert 'data' in fig
    assert 'layout' in fig

def test_sbl_domain_summary_statistics(sbl_data):
    domain = SblDomain(sbl_data)
    summary = sbl_data['loan_amount'].describe().to_dict()
    assert 'count' in summary
    assert summary['count'] == 3
    assert summary['mean'] == 123333.33333333333
