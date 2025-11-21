"""FastAPI Application for Sales Analytics"""
from fastapi import FastAPI, HTTPException
from models.database import db_manager
from config.logger import setup_logger
from config.settings import config

logger = setup_logger(__name__)

app = FastAPI(
    title="Sales Analytics API",
    description="API for querying sales performance data",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "name": "Sales Analytics API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
def health_check():
    try:
        db_manager.execute_query("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/api/v1/sales/metrics")
def get_sales_metrics():
    try:
        query = """
            SELECT 
                COUNT(*) as total_transactions,
                SUM(amount) as total_revenue,
                AVG(amount) as avg_transaction_value,
                SUM(CASE WHEN is_won = TRUE THEN amount ELSE 0 END) as won_revenue
            FROM fact_sales
        """
        result = db_manager.execute_query(query)
        
        if result and result[0]:
            row = result[0]
            return {
                "total_transactions": int(row[0] or 0),
                "total_revenue": float(row[1] or 0),
                "avg_transaction_value": float(row[2] or 0),
                "won_revenue": float(row[3] or 0)
            }
        return {"message": "No data available"}
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/customers")
def get_customers():
    try:
        query = "SELECT customer_name, industry, city, state FROM dim_customer LIMIT 10"
        results = db_manager.execute_query(query)
        
        return [
            {
                "customer_name": row[0],
                "industry": row[1],
                "city": row[2],
                "state": row[3]
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
