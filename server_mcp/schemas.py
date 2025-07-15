from typing import Dict, Any, Optional
from pydantic import BaseModel

class MongoDBSearchParams(BaseModel):
    operation: str
    filter: Optional[Dict[str, Any]] = {}
    limit: Optional[int] = 0
    sort: Optional[Dict[str, Any]] = None

