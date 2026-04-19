from pydantic import BaseModel, ConfigDict
from typing import Optional

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    mechanic_id: int
    mechanic_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
