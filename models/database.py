"""Database utilities"""
import psycopg2
import pandas as pd
from contextlib import contextmanager
from config.settings import config
from config.logger import setup_logger

logger = setup_logger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': config.DB_HOST,
            'port': config.DB_PORT,
            'database': config.DB_NAME,
            'user': config.DB_USER,
            'password': config.DB_PASSWORD
        }
    
    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = None):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
    
    def bulk_insert(self, table: str, df: pd.DataFrame):
        if df.empty:
            logger.warning(f"No data to insert into {table}")
            return 0
        
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        
        values = [tuple(row) for row in df.values]
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(query, values)
                rows_inserted = cur.rowcount
                logger.info(f"Inserted {rows_inserted} rows into {table}")
                return rows_inserted
    
    def query_to_dataframe(self, query: str, params: tuple = None):
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=params)
            return df

db_manager = DatabaseManager()
