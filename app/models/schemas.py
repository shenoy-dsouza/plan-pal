from pydantic import BaseModel
from typing import Optional


class TripRequest(BaseModel):
    destination: str
    budget: int
    days: int
    style: Optional[str] = None
