# Sales API Pipeline

A comprehensive data engineering project demonstrating ETL pipeline development, API integration, and data warehousing.

## 🎯 Project Overview

This project extracts data from multiple sources (Salesforce, Stripe, Google Sheets), transforms it into a dimensional model, and loads it into a database for analytics.

## ✨ Features

- **Multi-Source Data Integration**: Connects to Salesforce (CRM), Stripe (payments), and Google Sheets (manual data)
- **ETL Pipeline**: Automated extraction, transformation, and loading of sales data
- **Dimensional Data Model**: Star schema with fact and dimension tables
- **Mock Connectors**: Test the pipeline without API credentials
- **REST API**: FastAPI endpoints for querying analytics
- **SQLite Database**: Lightweight database for local development

## 🏗️ Architecture
```
┌─────────────┐
│ Salesforce  │──┐
└─────────────┘  │
                 │
┌─────────────┐  │    ┌──────────┐    ┌──────────┐
│   Stripe    │──┼───▶│   ETL    │───▶│  SQLite  │
└─────────────┘  │    │ Pipeline │    │ Database │
                 │    └──────────┘    └──────────┘
┌─────────────┐  │
│   Google    │──┘
│   Sheets    │
└─────────────┘
```

## 🛠️ Tech Stack

- **Python 3.13**
- **pandas** - Data manipulation
- **SQLite** - Database
- **FastAPI** - REST API framework
- **uvicorn** - ASGI server

## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/sales-api-pipeline.git
cd sales-api-pipeline

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

## 🚀 Usage

### Run the ETL Pipeline
```bash
python3 run_pipeline_simple.py
```

**Output:**
- Extracts data from 3 mock APIs
- Loads data into SQLite database
- Displays metrics (customers, products, revenue)

### Query the Database
```bash
sqlite3 sales_analytics.db

SELECT * FROM dim_customer;
SELECT * FROM fact_sales;
```

### Start the API (Optional)
```bash
python3 api_simple.py
```

Visit: http://localhost:8001/docs for interactive API documentation

## 📊 Data Model

### Dimension Tables
- `dim_customer` - Customer master data
- `dim_product` - Product catalog
- `dim_territory` - Sales territories
- `dim_sales_rep` - Sales representatives

### Fact Tables
- `fact_sales` - Sales transactions and metrics

## 🎓 Skills Demonstrated

- **Data Engineering**: ETL pipeline development, data modeling
- **API Integration**: OAuth, REST APIs, rate limiting
- **Python**: OOP, pandas, error handling, logging
- **SQL**: Database design, queries, joins
- **Software Engineering**: Modular code, configuration management

## 📈 Results

Pipeline successfully processes:
- 3 customers
- 5 products  
- 8 sales transactions
- $150,000 total revenue tracked

## 🔧 Project Structure
```
sales_api_pipeline/
├── connectors/           # API connector classes
│   ├── salesforce_connector.py
│   ├── stripe_connector.py
│   └── google_sheets_connector.py
├── etl/                  # ETL pipeline logic
├── models/               # Database utilities
├── api/                  # FastAPI application
├── config/               # Configuration management
├── run_pipeline_simple.py # Main pipeline script
└── requirements.txt      # Dependencies
```

## 🤝 Contributing

This is a portfolio project, but feedback is welcome!

## 📝 License

MIT License

## 👤 Author

**Chima Ojini**
- Data Engineer
- Specializing in ETL pipelines and data integration

---

*Built as a portfolio project demonstrating end-to-end data engineering capabilities*
