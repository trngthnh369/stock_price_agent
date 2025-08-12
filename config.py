"""
Configuration module for Stock Price Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')
    
    # API URLs
    POLYGON_BASE_URL = "https://api.polygon.io"
    
    # Rate limiting settings
    API_DELAY = 0.5  # seconds between API calls
    RATE_LIMIT_DELAY = 60  # seconds to wait when rate limited
    
    # Gemini Model
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    # Default settings
    DEFAULT_HISTORICAL_DAYS = 30
    DEFAULT_CHART_FIGSIZE = (10, 6)
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        missing_keys = []
        
        if not cls.GEMINI_API_KEY:
            missing_keys.append('GEMINI_API_KEY')
            
        if not cls.POLYGON_API_KEY:
            missing_keys.append('POLYGON_API_KEY')
            
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
        
        return True