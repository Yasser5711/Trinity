from sqlalchemy.orm import Session
from db.models.models import KPI


def get_all(db: Session):
    return db.query(KPI).all()


def get_by_id(db: Session, kpi_id: int):
    return db.query(KPI).filter(KPI.id == kpi_id).first()


def create(db: Session, kpi: KPI):
    db.add(kpi)
    db.commit()
    db.refresh(kpi)
    return kpi


def update(db: Session, kpi: KPI):
    db.commit()
    db.refresh(kpi)
    return kpi


def delete(db: Session, kpi: KPI):
    db.delete(kpi)
    db.commit()
