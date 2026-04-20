from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)
    
    data: T
    message: Optional[str] = None
