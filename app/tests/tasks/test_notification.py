import pytest

from datetime import datetime, timedelta

from unittest import mock

from app import schemas
from app.crud import user as crud_user
from app.crud import notification as crud_notification
from app.models import Notification
from app.tasks.notification import schedule_failed_notifications, send_notification


@mock.patch("app.tasks.notification.random.choice")
def test_send_notification_failed(random_choice_mock, db_session):
    random_choice_mock.return_value = 0

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

    with pytest.raises(Exception):
        send_notification(notification.id)

    db_session.refresh(notification)

    assert notification.status == schemas.StatusEnum.failed


@mock.patch("app.tasks.notification.random.choice")
def test_send_notification_ok(random_choice_mock, db_session):
    random_choice_mock.return_value = 1

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

    send_notification(notification.id)

    db_session.refresh(notification)

    assert notification.status == schemas.StatusEnum.done


@mock.patch("app.tasks.notification.send_notification.delay")
def test_schedule_failed_notifications(send_notification_mock, db_session):
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
        (datetime.utcnow() - timedelta(hours=6, minutes=1), schemas.StatusEnum.in_progress),
        (datetime.utcnow() - timedelta(hours=5, minutes=1), schemas.StatusEnum.failed),
        (datetime.utcnow() - timedelta(hours=2, minutes=1), schemas.StatusEnum.new),
    ]
    for created_at, status in data:
        d = {
            "user_id": user_id,
            "notification_type": "email",
            "subject": "Hi!",
            "content": {"type": "random"},
            "created_at": created_at,
            "status": status,
        }
        db_session.add(Notification(**d))
    db_session.commit()

    schedule_failed_notifications()
    assert send_notification_mock.call_count == 3
