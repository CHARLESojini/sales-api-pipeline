"""Test just the connectors without database"""
from connectors.salesforce_connector import MockSalesforceConnector
from connectors.stripe_connector import MockStripeConnector
from connectors.google_sheets_connector import MockGoogleSheetsConnector

print("Testing Salesforce...")
with MockSalesforceConnector() as sf:
    accounts = sf.get_accounts()
    print(f"✅ Got {len(accounts)} accounts")
    print(accounts.head())

print("\nTesting Stripe...")
with MockStripeConnector() as stripe:
    charges = stripe.get_charges()
    print(f"✅ Got {len(charges)} charges")
    print(charges.head())

print("\nTesting Google Sheets...")
with MockGoogleSheetsConnector() as gs:
    products = gs.get_products()
    print(f"✅ Got {len(products)} products")
    print(products.head())

print("\n🎉 All connectors working!")
