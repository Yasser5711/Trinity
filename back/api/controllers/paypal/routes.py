from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.helpers import get_db, login_required
from db.models.models import User
from external import paypal_client
from services import paypal_service

router = APIRouter()


@router.get("/test-paypal-token", tags=["paypal"])
def test_token():
    return {"token": paypal_client.get_paypal_token()}


@router.post(
    "/create-paypal-order", status_code=status.HTTP_201_CREATED, tags=["paypal"]
)
def create_order(
    current_user: User = Depends(login_required), db: Session = Depends(get_db)
):
    try:
        return paypal_service.create_paypal_order(db, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/capture-paypal-order/{order_id}", tags=["paypal"])
def capture_order(
    order_id: str,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db),
):
    try:
        return paypal_service.capture_paypal_order(db, current_user.id, order_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
