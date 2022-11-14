from typing import Optional

from sqlalchemy.orm import Session

from app import schemas
from app.models import Notification, User
from app.crud import user as crud_user
from app.crud import notification as crud_notification


def create_user_factory(
        db: Session,
        id: Optional[int] = 1,
        email: Optional[str] = "random@gmail.com",
        country_code: Optional[int] = 22,
        phone_number: Optional[int] = 3333333,
) -> User:
    return crud_user.create_user(
        db,
        schemas.UserCreate(
            id=id,
            email=email,
            country_code=country_code,
            phone_number=phone_number,
        ),
    )


def create_notification_factory(
    db: Session,
    user_id: Optional[int] = None,
    subject: Optional[str] = "Text",
    content: Optional[dict] = None,
    notification_type: Optional[schemas.NotificationTypeEnum.email] = schemas.NotificationTypeEnum.email,
) -> Notification:
    return crud_notification.create_user_notification(
        db,
        schemas.NotificationCreate(
            subject=subject,
            content=content or {"type": "random"},
            notification_type=notification_type,
            user_id=user_id or create_user_factory(db).id,
        ),
    )

