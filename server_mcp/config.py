from pydantic_settings import BaseSettings

class MCPSettings(BaseSettings):
    """Settings for MCP server."""
    postgres_dsn: str

    class Config:
        env_file = ".env"

settings = MCPSettings()
