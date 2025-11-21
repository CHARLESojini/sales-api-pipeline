"""Salesforce API Connector with Mock Data"""
import pandas as pd
from datetime import datetime
from config.logger import setup_logger

logger = setup_logger(__name__)

class MockSalesforceConnector:
    def authenticate(self) -> bool:
        logger.info("Using mock Salesforce connector")
        return True
    
    def get_accounts(self, modified_since=None):
        data = {
            'customer_id': ['SF001', 'SF002', 'SF003'],
            'customer_name': ['Acme Corp', 'TechStart Inc', 'Global Pharma'],
            'customer_type': ['Customer', 'Prospect', 'Customer'],
            'industry': ['Technology', 'Healthcare', 'Pharmaceutical'],
            'city': ['San Francisco', 'Boston', 'New York'],
            'state': ['CA', 'MA', 'NY'],
            'country': ['USA', 'USA', 'USA'],
            'email': ['contact@acme.com', 'info@techstart.com', 'sales@globalpharma.com'],
            'phone': ['555-0101', '555-0102', '555-0103'],
            'created_date': pd.to_datetime(['2023-01-15', '2023-03-20', '2023-02-10']),
            'last_modified_date': pd.to_datetime(['2024-11-01', '2024-10-15', '2024-11-10'])
        }
        logger.info(f"Extracted {len(data['customer_id'])} accounts from Salesforce")
        return pd.DataFrame(data)
    
    def get_opportunities(self, modified_since=None):
        data = {
            'opportunity_id': ['OPP001', 'OPP002', 'OPP003', 'OPP004'],
            'opportunity_name': ['Q4 Deal', 'License Renewal', 'New Product', 'Consulting'],
            'customer_id': ['SF001', 'SF003', 'SF002', 'SF001'],
            'stage': ['Proposal', 'Closed Won', 'Negotiation', 'Qualification'],
            'amount': [250000, 75000, 150000, 50000],
            'probability': [60, 100, 70, 30],
            'close_date': pd.to_datetime(['2024-12-31', '2024-11-15', '2024-12-20', '2025-01-15']),
            'is_closed': [False, True, False, False],
            'is_won': [False, True, False, False],
            'created_date': pd.to_datetime(['2024-10-01', '2024-09-15', '2024-10-20', '2024-11-01']),
            'last_modified_date': pd.to_datetime(['2024-11-18', '2024-11-15', '2024-11-19', '2024-11-05'])
        }
        logger.info(f"Extracted {len(data['opportunity_id'])} opportunities from Salesforce")
        return pd.DataFrame(data)
    
    def __enter__(self):
        self.authenticate()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
