from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.helpers import get_db, has_role
from services import report_service

router = APIRouter()


@router.get("/reports", tags=["reports"])
def generate_report(
    db: Session = Depends(get_db),
    current_user=Depends(has_role("admin"))
):
    return report_service.generate_report(db)
