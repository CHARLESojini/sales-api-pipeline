"""Simplified pipeline using SQLite"""
import sqlite3
from datetime import datetime
from connectors.salesforce_connector import MockSalesforceConnector
from connectors.stripe_connector import MockStripeConnector
from connectors.google_sheets_connector import MockGoogleSheetsConnector

print("=" * 80)
print("SALES API PIPELINE (SQLite version)")
print("=" * 80)
print(f"Started: {datetime.now()}")
print("=" * 80)

# Create SQLite database
conn = sqlite3.connect('sales_analytics.db')
cursor = conn.cursor()

# Create tables
print("\nCreating tables...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT UNIQUE NOT NULL,
    customer_name TEXT NOT NULL,
    industry TEXT,
    city TEXT,
    state TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_product (
    product_key INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT UNIQUE NOT NULL,
    product_name TEXT NOT NULL,
    product_category TEXT,
    unit_price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    amount REAL,
    is_won INTEGER,
    transaction_date TEXT
)
""")

conn.commit()
print("✅ Tables created")

# Extract data
print("\nExtracting from Salesforce...")
with MockSalesforceConnector() as sf:
    accounts = sf.get_accounts()
    opportunities = sf.get_opportunities()
    
print(f"✅ Extracted {len(accounts)} accounts, {len(opportunities)} opportunities")

print("\nExtracting from Stripe...")
with MockStripeConnector() as stripe:
    charges = stripe.get_charges()
print(f"✅ Extracted {len(charges)} charges")

print("\nExtracting from Google Sheets...")
with MockGoogleSheetsConnector() as gs:
    products = gs.get_products()
print(f"✅ Extracted {len(products)} products")

# Load customers
print("\nLoading customers...")
for _, row in accounts.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO dim_customer (customer_id, customer_name, industry, city, state, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (row['customer_id'], row['customer_name'], row['industry'], 
          row['city'], row['state'], row['email']))

# Load products
print("Loading products...")
for _, row in products.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO dim_product (product_id, product_name, product_category, unit_price)
        VALUES (?, ?, ?, ?)
    """, (row['product_id'], row['product_name'], row['product_category'], row['unit_price']))

# Load sales facts
print("Loading sales facts...")
for _, row in opportunities.iterrows():
    cursor.execute("""
        INSERT INTO fact_sales (customer_id, amount, is_won, transaction_date)
        VALUES (?, ?, ?, ?)
    """, (row['customer_id'], row['amount'], int(row['is_won']), str(row['close_date'])))

conn.commit()

# Show results
print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

cursor.execute("SELECT COUNT(*) FROM dim_customer")
print(f"Customers loaded: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM dim_product")
print(f"Products loaded: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM fact_sales")
print(f"Sales transactions loaded: {cursor.fetchone()[0]}")

cursor.execute("SELECT SUM(amount) FROM fact_sales WHERE is_won = 1")
total_revenue = cursor.fetchone()[0]
print(f"Total revenue (won deals): ${total_revenue:,.2f}")

print("\n🎉 Pipeline completed successfully!")
print("=" * 80)

conn.close()
