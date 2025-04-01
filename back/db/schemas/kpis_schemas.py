from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .schemas import KPI as KPIBase


class KPICreate(KPIBase):
    name: str
    value: float


class KPIUpdate(KPIBase):
    name: Optional[str] = None
    value: Optional[float] = None


class KPIResponse(KPIBase):
    id: int
    value: float
