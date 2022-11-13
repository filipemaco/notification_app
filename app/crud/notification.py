from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


def get_notification(
    db: Session, notification_id: int
) -> Optional[models.Notification]:
    return (
        db.query(models.Notification)
        .filter(models.Notification.id == notification_id)
        .first()
    )


def get_notifications(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Notification]:
    return db.query(models.Notification).offset(skip).limit(limit).all()


def create_user_notification(
    db: Session, notification: schemas.NotificationCreate
) -> models.Notification:
    db_notification = models.Notification(
        status=schemas.StatusEnum.new.value, **notification.dict()
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def update_notification_status(
    db: Session, notification_id: int, status: schemas.StatusEnum
):
    db.query(models.Notification).filter(
        models.Notification.id == notification_id
    ).update({"status": status})
    db.commit()


def get_stuck_notifications(db: Session) -> List[models.Notification.id]:
    two_hours_ago = datetime.utcnow() - timedelta(hours=2)

    return (
        db.query(models.Notification.id)
        .filter(
            models.Notification.status != schemas.StatusEnum.done,
            models.Notification.created_at < two_hours_ago,
        )
        .all()
    )
