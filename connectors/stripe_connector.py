"""Stripe API Connector with Mock Data"""
import pandas as pd
from datetime import datetime
from config.logger import setup_logger

logger = setup_logger(__name__)

class MockStripeConnector:
    def authenticate(self) -> bool:
        logger.info("Using mock Stripe connector")
        return True
    
    def get_charges(self, created_since=None):
        data = {
            'charge_id': ['CH001', 'CH002', 'CH003', 'CH004', 'CH005'],
            'customer_id': ['SF001', 'SF003', 'SF002', 'SF001', 'SF003'],
            'amount': [250000, 75000, 150000, 50000, 125000],
            'currency': ['USD', 'USD', 'USD', 'USD', 'USD'],
            'status': ['succeeded', 'succeeded', 'succeeded', 'pending', 'succeeded'],
            'paid': [True, True, True, False, True],
            'created': pd.to_datetime(['2024-11-01', '2024-11-15', '2024-10-20', '2024-11-05', '2024-11-18']),
        }
        logger.info(f"Extracted {len(data['charge_id'])} charges from Stripe")
        return pd.DataFrame(data)
    
    def __enter__(self):
        self.authenticate()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
