from pydantic import BaseModel

class TableDetailsParams(BaseModel):
    """Parameters to get detailed information about a table."""
    table_name: str
