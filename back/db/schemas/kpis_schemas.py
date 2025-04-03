from typing import Optional

from .schemas import KPI as KPIBase  # noqa: N811


class KPICreate(KPIBase):
    name: str
    value: float


class KPIUpdate(KPIBase):
    name: Optional[str] = None
    value: Optional[float] = None


class KPIResponse(KPIBase):
    id: int
    value: float
