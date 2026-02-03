from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str = "postgresql://pmanalytics:devpassword@localhost:5432/pm_analytics"

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PM Analytics API"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"

    # Environment
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # Data quality
    MIN_CONFIDENCE_SCORE: float = 1.0  # Only display 100% confidence data

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
