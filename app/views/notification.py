from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import notification as crud_notification
from app.crud import user as crud_user
from app.dependencies import get_db
from app.tasks.notification import send_notification

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Notification])
def get_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_notification.get_notifications(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Notification, summary="Create a notification")
def create_notification_for_user(
    notification: schemas.NotificationCreate, db: Session = Depends(get_db)
):
    if not crud_user.get_user(db, user_id=notification.user_id):
        raise HTTPException(status_code=400, detail="User does not exist")

    notification_db = crud_notification.create_user_notification(
        db=db, notification=notification
    )

    send_notification.delay(notification_db.id)

    return notification_db


@router.get("/{notification_id}", response_model=schemas.Notification)
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud_notification.get_notification(
        db, notification_id=notification_id
    )
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification


notifications_router = router
