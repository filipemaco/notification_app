from sqlalchemy.orm import Session

from app import models, schemas


def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Notification).offset(skip).limit(limit).all()


def create_user_notification(db: Session, device: schemas.NotificationCreate):
    db_item = models.Notification(**device.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
