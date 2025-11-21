-- Sales Analytics Data Warehouse Schema
-- Star Schema Design

-- Drop existing tables
DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_sales_rep CASCADE;
DROP TABLE IF EXISTS dim_territory CASCADE;
DROP TABLE IF EXISTS etl_log CASCADE;

-- Customer Dimension
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_type VARCHAR(50),
    industry VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50),
    created_date TIMESTAMP,
    last_modified_date TIMESTAMP
);

-- Product Dimension
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_category VARCHAR(100),
    unit_price DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP,
    last_modified_date TIMESTAMP
);

-- Date Dimension
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    day_of_month INTEGER,
    month INTEGER,
    month_name VARCHAR(10),
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN
);

-- Territory Dimension
CREATE TABLE dim_territory (
    territory_key SERIAL PRIMARY KEY,
    territory_name VARCHAR(100) UNIQUE NOT NULL,
    region VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
);

-- Sales Rep Dimension
CREATE TABLE dim_sales_rep (
    sales_rep_key SERIAL PRIMARY KEY,
    sales_rep_name VARCHAR(255) NOT NULL,
    territory_key INTEGER,
    region VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
);

-- Sales Fact Table
CREATE TABLE fact_sales (
    sales_key SERIAL PRIMARY KEY,
    date_key INTEGER,
    customer_key INTEGER,
    product_key INTEGER,
    sales_rep_key INTEGER,
    territory_key INTEGER,
    amount DECIMAL(15, 2) NOT NULL,
    quantity INTEGER DEFAULT 1,
    is_won BOOLEAN DEFAULT FALSE,
    is_closed BOOLEAN DEFAULT FALSE,
    transaction_date TIMESTAMP NOT NULL,
    source_system VARCHAR(50),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (sales_rep_key) REFERENCES dim_sales_rep(sales_rep_key),
    FOREIGN KEY (territory_key) REFERENCES dim_territory(territory_key)
);

-- ETL Log Table
CREATE TABLE etl_log (
    log_id SERIAL PRIMARY KEY,
    etl_process VARCHAR(100) NOT NULL,
    source_system VARCHAR(50),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(20),
    records_processed INTEGER,
    records_inserted INTEGER,
    error_message TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate Date Dimension
INSERT INTO dim_date (date_key, full_date, day_of_week, day_name, day_of_month, month, month_name, quarter, year, is_weekend)
SELECT 
    TO_CHAR(date_series, 'YYYYMMDD')::INTEGER,
    date_series::DATE,
    EXTRACT(DOW FROM date_series)::INTEGER,
    TO_CHAR(date_series, 'Day'),
    EXTRACT(DAY FROM date_series)::INTEGER,
    EXTRACT(MONTH FROM date_series)::INTEGER,
    TO_CHAR(date_series, 'Month'),
    EXTRACT(QUARTER FROM date_series)::INTEGER,
    EXTRACT(YEAR FROM date_series)::INTEGER,
    EXTRACT(DOW FROM date_series) IN (0, 6)
FROM generate_series('2023-01-01'::DATE, '2027-12-31'::DATE, '1 day'::INTERVAL) AS date_series;

-- Create indexes
CREATE INDEX idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);

-- Success message
SELECT 'Schema created successfully! Date dimension populated with ' || COUNT(*) || ' dates.' 
FROM dim_date;
