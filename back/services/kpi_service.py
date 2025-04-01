from sqlalchemy.orm import Session
from db.models.models import KPI
from db.schemas.kpis_schemas import KPICreate, KPIUpdate
from repositories import kpi_repository


def get_all_kpis(db: Session):
    return kpi_repository.get_all(db)


def get_kpi_by_id(db: Session, kpi_id: int):
    kpi = kpi_repository.get_by_id(db, kpi_id)
    if not kpi:
        raise ValueError("KPI not found")
    return kpi


def create_kpi(db: Session, data: KPICreate):
    kpi = KPI(name=data.name, value=data.value)
    return kpi_repository.create(db, kpi)


def update_kpi(db: Session, kpi_id: int, data: KPIUpdate):
    kpi = kpi_repository.get_by_id(db, kpi_id)
    if not kpi:
        raise ValueError("KPI not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(kpi, key, value)

    return kpi_repository.update(db, kpi)


def delete_kpi(db: Session, kpi_id: int):
    kpi = kpi_repository.get_by_id(db, kpi_id)
    if not kpi:
        raise ValueError("KPI not found")

    kpi_repository.delete(db, kpi)
