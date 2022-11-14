from datetime import datetime, timedelta
from unittest import mock

import pytest

from app import schemas
from app.models import Notification
from app.tasks.notification import (schedule_failed_notifications,
                                    send_notification)
from app.tests.utils import create_notification_factory, create_user_factory


@mock.patch("app.tasks.notification.random.choice")
def test_send_notification_failed(random_choice_mock, db_session):
    random_choice_mock.return_value = True
    notification = create_notification_factory(db_session)

    with pytest.raises(Exception):
        send_notification(notification.id)

    db_session.refresh(notification)

    assert notification.status == schemas.StatusEnum.failed


@mock.patch("app.tasks.notification.random.choice")
def test_send_notification_ok(random_choice_mock, db_session):
    random_choice_mock.return_value = False
    notification = create_notification_factory(db_session)

    send_notification(notification.id)

    db_session.refresh(notification)

    assert notification.status == schemas.StatusEnum.done


@mock.patch("app.tasks.notification.send_notification.delay")
def test_schedule_failed_notifications(send_notification_mock, db_session):
    user_id = create_user_factory(db_session).id
    data = [
        (
            datetime.utcnow() - timedelta(hours=6, minutes=1),
            schemas.StatusEnum.in_progress,
        ),
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
