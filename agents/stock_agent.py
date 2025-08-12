"""
Stock Data Agent - Fetches stock data from Polygon API
"""
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config import Config


class StockDataAgent:
    """
    Agent chính để lấy dữ liệu cổ phiếu từ Polygon API
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.POLYGON_API_KEY
        self.base_url = Config.POLYGON_BASE_URL
        
        if not self.api_key:
            raise ValueError("Polygon API key is required")

    def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Helper method to make API requests with rate limiting
        """
        # Add delay to prevent rate limiting
        time.sleep(Config.API_DELAY)
        
        params['apikey'] = self.api_key
        response = requests.get(url, params=params)
        
        # Handle rate limiting
        if response.status_code == 429:
            print(f"⚠️ Rate limit reached. Waiting {Config.RATE_LIMIT_DELAY} seconds...")
            time.sleep(Config.RATE_LIMIT_DELAY)
            response = requests.get(url, params=params)
        
        response.raise_for_status()
        return response.json()

    def get_daily_open_close(self, symbol: str, date: str) -> Dict[str, Any]:
        """
        Lấy dữ liệu open/close theo ngày cho một cổ phiếu

        Args:
            symbol: Mã cổ phiếu (VD: AAPL)
            date: Ngày theo format YYYY-MM-DD

        Returns:
            Dict chứa thông tin open, close, high, low, volume
        """
        try:
            url = f"{self.base_url}/v1/open-close/{symbol}/{date}"
            data = self._make_request(url, {})

            if data.get("status") == "OK":
                return {
                    "symbol": data.get("symbol"),
                    "date": data.get("from"),
                    "open": data.get("open"),
                    "close": data.get("close"),
                    "high": data.get("high"),
                    "low": data.get("low"),
                    "volume": data.get("volume"),
                    "pre_market": data.get("preMarket"),
                    "after_hours": data.get("afterHours")
                }
            else:
                return {"error": "Không thể lấy dữ liệu", "details": data}

        except Exception as e:
            return {"error": str(e)}

    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Lấy giá hiện tại của cổ phiếu
        """
        try:
            url = f"{self.base_url}/v2/aggs/ticker/{symbol}/prev"
            data = self._make_request(url, {})

            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                return {
                    "symbol": symbol,
                    "close": result.get("c"),
                    "open": result.get("o"),
                    "high": result.get("h"),
                    "low": result.get("l"),
                    "volume": result.get("v"),
                    "timestamp": result.get("t")
                }
            else:
                return {"error": "Không thể lấy dữ liệu hiện tại"}

        except Exception as e:
            return {"error": str(e)}

    def get_historical_data(self, symbol: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Lấy dữ liệu lịch sử trong N ngày gần đây
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            url = f"{self.base_url}/v2/aggs/ticker/{symbol}/range/1/day/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
            params = {
                "adjusted": "true",
                "sort": "asc"
            }
            
            data = self._make_request(url, params)

            if data.get("status") == "OK" and data.get("results"):
                historical_data = []
                for result in data["results"]:
                    historical_data.append({
                        "date": datetime.fromtimestamp(result["t"]/1000).strftime('%Y-%m-%d'),
                        "open": result.get("o"),
                        "close": result.get("c"),
                        "high": result.get("h"),
                        "low": result.get("l"),
                        "volume": result.get("v")
                    })
                return historical_data
            else:
                return []

        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu lịch sử: {e}")
            return []