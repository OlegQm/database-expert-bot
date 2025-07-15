"""
This module defines the configuration settings for the application using Pydantic's BaseSettings.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class for application configuration.
    This class inherits from BaseSettings and is used to manage application
    configuration through environment variables. The configuration includes
    API keys, model names, database connection details, and vector search settings.

    Attributes:
        openai_api_key (str): API key for OpenAI services.

    Config:
        env_file (str): Path to the environment file containing configuration variables.

    """

    openai_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
