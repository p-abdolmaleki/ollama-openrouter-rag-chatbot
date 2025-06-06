from pydantic import BaseModel
from typing import Any, Optional

class ApiResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None