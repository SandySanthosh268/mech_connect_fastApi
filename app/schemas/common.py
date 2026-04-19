from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    """
    Standardize the JSON response wrapper to always return {"data": { ... }} 
    as expected by the React frontend Axios implementation.
    """
    model_config = ConfigDict(from_attributes=True)
    
    data: T
    message: Optional[str] = None
