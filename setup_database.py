"""Setup database without needing command line tools"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("Attempting to connect to PostgreSQL...")

# Try different connection methods
connection_attempts = [
    {'host': 'localhost', 'port': 5432, 'user': 'chimaojini', 'database': 'postgres'},
    {'host': 'localhost', 'port': 5432, 'database': 'postgres'},
    {'host': '127.0.0.1', 'port': 5432, 'user': 'chimaojini', 'database': 'postgres'},
    {'host': '127.0.0.1', 'port': 5432, 'database': 'postgres'},
]

conn = None
for i, params in enumerate(connection_attempts):
    try:
        print(f"Attempt {i+1}: {params}")
        conn = psycopg2.connect(**params)
        print(f"✅ Connected successfully!")
        break
    except Exception as e:
        print(f"   Failed: {e}")
        continue

if not conn:
    print("\n❌ Could not connect to PostgreSQL")
    print("Let's use SQLite instead - it requires no setup!")
    exit(1)

try:
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Drop and create database
    print("\nCreating database...")
    cursor.execute("DROP DATABASE IF EXISTS sales_analytics")
    cursor.execute("CREATE DATABASE sales_analytics")
    print("✅ Database 'sales_analytics' created!")
    
    cursor.close()
    conn.close()
    
    # Connect to new database and load schema
    print("\nLoading schema...")
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='sales_analytics'
    )
    
    with open('schema.sql', 'r') as f:
        schema = f.read()
    
    cursor = conn.cursor()
    cursor.execute(schema)
    conn.commit()
    
    print("✅ Schema loaded successfully!")
    print("\n🎉 Database setup complete!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error during setup: {e}")
