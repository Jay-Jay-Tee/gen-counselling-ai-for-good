"""
Configuration Management
Handles environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "Genetic Risk Coach API"
    API_VERSION: str = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg",
        "image/png", 
        "image/jpg",
        "application/pdf"
    ]
    
    # AI Module Configuration
    AI_MODULE_PATH: str = "../ai"
    
    # Optional: Database Configuration
    # DATABASE_URL: str = "sqlite:///./genetic_risk.db"
    # Uncomment for PostgreSQL:
    # DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    
    # Optional: Authentication
    # SECRET_KEY: str = "your-secret-key-here"
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()


# Helper function to get settings
def get_settings() -> Settings:
    """
    Get application settings
    Usage: settings = get_settings()
    """
    return settings
