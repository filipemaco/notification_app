from sqlalchemy.orm import Session

from app import models, schemas


def get_notification(db: Session, notification_id: int):
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()


def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Notification).offset(skip).limit(limit).all()


def create_user_notification(db: Session, notification: schemas.NotificationCreate):
    db_notification = models.Notification(
        status=schemas.StatusEnum.new.value, **notification.dict()
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
