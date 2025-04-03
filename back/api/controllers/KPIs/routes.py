from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import get_db, has_role
from db.schemas.kpis_schemas import KPICreate, KPIResponse, KPIUpdate
from services import kpi_service

router = APIRouter()


@router.get("/kpis", response_model=list[KPIResponse], tags=["kpis"])
def get_kpis(db: Session = Depends(get_db), current_user=Depends(has_role("admin"))):
    return kpi_service.get_all_kpis(db)


@router.get("/kpis/{kpi_id}", response_model=KPIResponse, tags=["kpis"])
def get_kpi_by_id(
    kpi_id: int, db: Session = Depends(get_db), current_user=Depends(has_role("admin"))
):
    try:
        return kpi_service.get_kpi_by_id(db, kpi_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/kpis", status_code=status.HTTP_201_CREATED, tags=["kpis"])
def create_kpi(
    kpi: KPICreate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    return kpi_service.create_kpi(db, kpi)


@router.put("/kpis/{kpi_id}", tags=["kpis"])
def update_kpi(
    kpi_id: int,
    kpi: KPIUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin")),
):
    try:
        kpi_service.update_kpi(db, kpi_id, kpi)
        return {"message": "KPI updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/kpis/{kpi_id}", tags=["kpis"])
def delete_kpi(
    kpi_id: int, db: Session = Depends(get_db), current_user=Depends(has_role("admin"))
):
    try:
        kpi_service.delete_kpi(db, kpi_id)
        return {"message": "KPI deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
