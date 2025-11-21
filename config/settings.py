"""Configuration settings"""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    DB_NAME = os.getenv('DB_NAME', 'sales_analytics')
    DB_USER = os.getenv('DB_USER', os.getenv('USER', 'postgres'))
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '8000'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/pipeline.log')
    
    # Paths
    BASE_DIR = Path(_file_).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    LOG_DIR = BASE_DIR / 'logs'
    
    def _init_(self):
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOG_DIR.mkdir(exist_ok=True)

config = Config()
