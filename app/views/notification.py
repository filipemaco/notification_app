from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import notification as crud_notifications
from app.crud import user as crud_user
from app.dependencies import get_db

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Notification])
def get_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud_notifications.get_notifications(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Notification, summary="Create a notification")
def create_notification_for_user(
    notification: schemas.NotificationCreate, db: Session = Depends(get_db)
):
    if not crud_user.get_user(db, user_id=notification.user_id):
        raise HTTPException(status_code=400, detail="User does not exist")
    a = crud_notifications.create_user_notification(db=db, notification=notification)
    return a


notifications_router = router