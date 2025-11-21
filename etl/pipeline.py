"""Main ETL Pipeline"""
from datetime import datetime
from connector.salesforce_connector import MockSalesforceConnector
from connector.stripe_connector import MockStripeConnector
from connector.google_sheets_connector import MockGoogleSheetsConnector
from models.database import db_manager
from config.logger import setup_logger

logger = setup_logger(__name__)

class SalesDataPipeline:
    def __init__(self):
        self.stats = {
            'extracted': 0,
            'loaded': 0
        }
    
    def run_full_pipeline(self):
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info(f"Starting Sales Data Pipeline - {start_time}")
        logger.info("=" * 80)
        
        try:
            # Extract from Salesforce
            logger.info("Extracting from Salesforce...")
            with MockSalesforceConnector() as sf:
                accounts = sf.get_accounts()
                opportunities = sf.get_opportunities()
            
            # Extract from Stripe
            logger.info("Extracting from Stripe...")
            with MockStripeConnector() as stripe:
                charges = stripe.get_charges()
            
            # Extract from Google Sheets
            logger.info("Extracting from Google Sheets...")
            with MockGoogleSheetsConnector() as gs:
                products = gs.get_products()
                territories = gs.get_territories()
            
            # Load Customers
            logger.info("Loading customers...")
            db_manager.bulk_insert('dim_customer', accounts)
            
            # Load Products
            logger.info("Loading products...")
            db_manager.bulk_insert('dim_product', products)
            
            # Load Territories
            logger.info("Loading territories...")
            terr_df = territories[['territory_name', 'region']].drop_duplicates()
            db_manager.bulk_insert('dim_territory', terr_df)
            
            # Load Sales Reps
            logger.info("Loading sales reps...")
            rep_df = territories[['sales_rep_name', 'region']].drop_duplicates()
            db_manager.bulk_insert('dim_sales_rep', rep_df)
            
            # Load Sales Facts
            logger.info("Loading sales facts...")
            facts = self._prepare_facts(opportunities, charges)
            db_manager.bulk_insert('fact_sales', facts)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("=" * 80)
            logger.info(f"Pipeline completed successfully in {duration:.2f} seconds")
            logger.info("=" * 80)
            
            return {'status': 'SUCCESS', 'duration': duration}
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return {'status': 'FAILED', 'error': str(e)}
    
    def _prepare_facts(self, opportunities, charges):
        import pandas as pd
        
        # Prepare opportunity facts
        opp_facts = opportunities.copy()
        opp_facts['date_key'] = opp_facts['close_date'].apply(
            lambda x: int(pd.to_datetime(x).strftime('%Y%m%d')) if pd.notna(x) else None
        )
        
        # Get customer keys
        customer_map = db_manager.query_to_dataframe(
            "SELECT customer_key, customer_id FROM dim_customer"
        )
        
        opp_facts = opp_facts.merge(customer_map, on='customer_id', how='left')
        
        facts = pd.DataFrame({
            'date_key': opp_facts['date_key'],
            'customer_key': opp_facts['customer_key'],
            'amount': opp_facts['amount'],
            'is_won': opp_facts['is_won'],
            'is_closed': opp_facts['is_closed'],
            'transaction_date': opp_facts['close_date'],
            'source_system': 'Salesforce'
        })
        
        facts = facts.dropna(subset=['date_key', 'customer_key'])
        return facts

if __name__ == "__main__":
    pipeline = SalesDataPipeline()
    result = pipeline.run_full_pipeline()
    print(f"\nPipeline result: {result}")
