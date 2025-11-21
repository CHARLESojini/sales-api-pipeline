"""Simple API for Sales Analytics"""
from fastapi import FastAPI
import sqlite3

app = FastAPI(title="Sales Analytics API")

def get_db():
    conn = sqlite3.connect('sales_analytics.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    return {"name": "Sales Analytics API", "status": "active"}

@app.get("/health")
def health():
    try:
        conn = get_db()
        conn.execute("SELECT 1")
        conn.close()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/api/v1/customers")
def get_customers():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM dim_customer")
    customers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"customers": customers}

@app.get("/api/v1/sales/metrics")
def get_metrics():
    conn = get_db()
    cursor = conn.execute("SELECT COUNT(*), SUM(amount) FROM fact_sales")
    count, total = cursor.fetchone()
    conn.close()
    return {
        "total_transactions": count,
        "total_revenue": float(total or 0)
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting API on http://localhost:8000")
    print("📖 Docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)
