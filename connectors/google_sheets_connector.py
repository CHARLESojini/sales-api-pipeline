"""Google Sheets API Connector with Mock Data"""
import pandas as pd
from config.logger import setup_logger

logger = setup_logger(__name__)

class MockGoogleSheetsConnector:
    def authenticate(self) -> bool:
        logger.info("Using mock Google Sheets connector")
        return True
    
    def get_products(self):
        data = {
            'product_id': ['PROD001', 'PROD002', 'PROD003', 'PROD004', 'PROD005'],
            'product_name': ['Enterprise License', 'Pro Services', 'Cloud Hosting', 'Support Premium', 'Training'],
            'product_category': ['Software', 'Services', 'Infrastructure', 'Support', 'Services'],
            'unit_price': [50000, 25000, 12000, 5000, 8000],
            'is_active': [True, True, True, True, True]
        }
        logger.info(f"Extracted {len(data['product_id'])} products from Google Sheets")
        return pd.DataFrame(data)
    
    def get_territories(self):
        data = {
            'territory_name': ['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest'],
            'region': ['East', 'East', 'Central', 'West', 'Central'],
            'sales_rep_name': ['Alice Johnson', 'Bob Smith', 'Carol Williams', 'David Brown', 'Emma Davis']
        }
        logger.info(f"Extracted {len(data['territory_name'])} territories from Google Sheets")
        return pd.DataFrame(data)
    
    def __enter__(self):
        self.authenticate()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
