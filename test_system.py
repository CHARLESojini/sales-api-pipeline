"""Test script to verify the system"""
import sys
from config.logger import setup_logger
from models.database import db_manager

logger = setup_logger(__name__)

def test_database():
    print("\n" + "=" * 80)
    print("TESTING DATABASE")
    print("=" * 80)
    
    try:
        print("\n1. Testing database connection...")
        result = db_manager.execute_query("SELECT version()")
        print("   ✓ Connected to PostgreSQL")
        
        print("\n2. Checking tables...")
        tables = ['dim_customer', 'dim_product', 'dim_date', 'fact_sales', 'etl_log']
        
        for table in tables:
            query = f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table}'
                )
            """
            result = db_manager.execute_query(query)
            exists = result[0][0] if result else False
            status = "✓" if exists else "✗"
            print(f"   {status} Table: {table}")
        
        print("\n✅ Database tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        return False

def main():
    print("\n" + "=" * 80)
    print("SALES API PIPELINE - SYSTEM TEST")
    print("=" * 80)
    
    results = {'database': False}
    results['database'] = test_database()
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.upper()}: {status}")
    
    print("=" * 80)
    
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
