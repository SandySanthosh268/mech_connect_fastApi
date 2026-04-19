from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class VehicleBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: str = "CAR"
    brand: str
    model: str
    registration_number: Optional[str] = Field(None, alias="registrationNumber")

class VehicleCreate(VehicleBase):
    registrationNumber: Optional[str] = None

class VehicleResponse(VehicleBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
