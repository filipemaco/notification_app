from datetime import datetime, timedelta

from app import schemas
from app.crud import notification as crud_notification
from app.crud import user as crud_user
from app.models import Notification


def test_create_notification(db_session):
    user_id = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=44, email="random@gmail.com", country_code=22, phone_number=333333
        ),
    ).id

    subject = "hi"
    content = {"a": "b"}
    notification_type = schemas.NotificationTypeEnum.email.value

    notification = crud_notification.create_user_notification(
        db_session,
        schemas.NotificationCreate(
            user_id=user_id,
            subject=subject,
            content=content,
            notification_type=notification_type,
        ),
    )

    assert notification.user_id == user_id
    assert notification.status == schemas.StatusEnum.new.value
    assert notification.content == content
    assert notification.subject == subject
    assert notification.notification_type == notification_type


def test_get_notification(db_session):
    user_id = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=44, email="random@gmail.com", country_code=22, phone_number=333333
        ),
    ).id

    expected_notification = crud_notification.create_user_notification(
        db_session,
        schemas.NotificationCreate(
            user_id=user_id,
            subject="hi",
            content={"a": "b"},
            notification_type=schemas.NotificationTypeEnum.sms.value,
        ),
    )

    notification = crud_notification.get_notification(
        db_session, expected_notification.id
    )

    assert notification.user_id == user_id
    assert notification.subject == expected_notification.subject
    assert notification.content == expected_notification.content
    assert notification.notification_type == expected_notification.notification_type


def test_update_notification_status(db_session):
    user_id = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=11,
            email="random@gmail.com",
            country_code=22,
            phone_number=333333,
        ),
    ).id

    notification = crud_notification.create_user_notification(
        db_session,
        schemas.NotificationCreate(
            subject="Text",
            content={"random": "text"},
            notification_type=schemas.NotificationTypeEnum.email.value,
            user_id=user_id,
        ),
    )

    assert notification.status == schemas.StatusEnum.new

    crud_notification.update_notification_status(
        db_session, notification.id, schemas.StatusEnum.failed
    )
    db_session.refresh(notification)

    assert notification.status == schemas.StatusEnum.failed


def test_get_stuck_notifications(db_session):
    user_id = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=11,
            email="random@gmail.com",
            country_code=22,
            phone_number=333333,
        ),
    ).id

    data = [
        (1, datetime.utcnow(), schemas.StatusEnum.done),
        (2, datetime.utcnow(), schemas.StatusEnum.in_progress),
        (3, datetime.utcnow(), schemas.StatusEnum.failed),
        (4, datetime.utcnow(), schemas.StatusEnum.new),
        (5, datetime.utcnow() - timedelta(hours=2, minutes=1), schemas.StatusEnum.done),
        (
            6,
            datetime.utcnow() - timedelta(hours=2, minutes=1),
            schemas.StatusEnum.in_progress,
        ),
        (
            7,
            datetime.utcnow() - timedelta(hours=2, minutes=1),
            schemas.StatusEnum.failed,
        ),
        (8, datetime.utcnow() - timedelta(hours=2, minutes=1), schemas.StatusEnum.new),
    ]

    for id, created_at, status in data:
        d = {
            "id": id,
            "user_id": user_id,
            "notification_type": "email",
            "subject": "Hi!",
            "content": {"type": "random"},
            "created_at": created_at,
            "status": status,
        }
        db_session.add(Notification(**d))

    db_session.commit()

    assert all(
        notification.id in (6, 7, 8)
        for notification in crud_notification.get_stuck_notifications(db_session)
    )
