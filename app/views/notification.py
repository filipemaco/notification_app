from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app import schemas
from app.crud.notification import get_notifications, create_user_notification
from app.dependencies import get_db

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Notification])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_notifications(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Notification)
def create_item_for_user(device: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return create_user_notification(db=db, device=device)


notifications_router = router
