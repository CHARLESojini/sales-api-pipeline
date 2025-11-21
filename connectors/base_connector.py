"""Base API Connector"""
import time
import requests
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from config.logger import setup_logger

logger = setup_logger(__name__)

class BaseAPIConnector(ABC):
    def __init__(self, base_url: str, rate_limit_calls: int = 100, rate_limit_period: int = 60):
        self.base_url = base_url
        self.session = requests.Session()
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period = rate_limit_period
        self._request_times = []
    
    @abstractmethod
    def authenticate(self) -> bool:
        pass
    
    def _check_rate_limit(self):
        current_time = time.time()
        self._request_times = [t for t in self._request_times if current_time - t < self.rate_limit_period]
        
        if len(self._request_times) >= self.rate_limit_calls:
            sleep_time = self.rate_limit_period - (current_time - self._request_times[0])
            if sleep_time > 0:
                logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                self._request_times = []
        
        self._request_times.append(current_time)
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                      data: Optional[Dict] = None, json: Optional[Dict] = None, 
                      headers: Optional[Dict] = None, retry_count: int = 3):
        self._check_rate_limit()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(retry_count):
            try:
                response = self.session.request(
                    method=method, url=url, params=params, data=data,
                    json=json, headers=headers, timeout=30
                )
                response.raise_for_status()
                try:
                    return response.json()
                except ValueError:
                    return {"data": response.text}
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error on attempt {attempt + 1}/{retry_count}: {e}")
                if attempt == retry_count - 1:
                    raise
                time.sleep(2 ** attempt)
        
        raise Exception(f"Failed after {retry_count} attempts")
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs):
        return self._make_request('GET', endpoint, params=params, **kwargs)
    
    def __enter__(self):
        self.authenticate()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
