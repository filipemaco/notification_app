from unittest import mock

from app import schemas
from app.tasks.notification import send_notification
from app.tests.utils import create_notification_factory, create_user_factory


def test_get_notifications_ok(client, db_session):
    # Create five users and ten notifications
    for i in range(1, 6):
        create_user_factory(
            db=db_session,
            id=i,
            email=f"random{i}@gmail.com",
            country_code=22 + i,
            phone_number=333333 + i,
        )

        for _ in range(2):
            create_notification_factory(db=db_session, user_id=i)

    response = client.get("/notifications/")

    assert response.status_code == 200
    assert len(response.json()) == 10


def test_create_notification_ok(client, db_session, settings, monkeypatch):
    user = create_user_factory(db_session)
    notification = schemas.NotificationCreate(
        subject="Text",
        content={"random": "text"},
        notification_type=schemas.NotificationTypeEnum.sms.value,
        user_id=user.id,
    )

    task_send_notification = mock.MagicMock(name="task_send_notification")
    monkeypatch.setattr(send_notification, "delay", task_send_notification)

    response = client.post("/notifications/", json=notification.dict())
    content = response.json()

    assert response.status_code == 200
    assert content["status"] == schemas.StatusEnum.new.value
    assert content["subject"] == notification.subject
    assert content["notification_type"] == notification.notification_type
    assert content["user_id"] == user.id
    task_send_notification.assert_called_with(content["id"])


def test_create_notification_with_wrong_user_id_failed(client, db_session):
    notification = schemas.NotificationCreate(
        subject="Text",
        content={"random": "text"},
        notification_type=schemas.NotificationTypeEnum.sms.value,
        user_id=1,
    )

    response = client.post("/notifications/", json=notification.dict())

    assert response.status_code == 400
    assert response.json()["detail"] == "User does not exist"


def test_get_notification_ok(client, db_session):
    notification = create_notification_factory(db=db_session)

    response = client.get(f"/notifications/{notification.id}")
    content = response.json()

    assert response.status_code == 200
    assert content["status"] == schemas.StatusEnum.new.value
    assert content["subject"] == notification.subject
    assert content["notification_type"] == notification.notification_type


def test_get_nonexistent_notification_failed(client, db_session):
    response = client.get("/notifications/2")

    assert response.status_code == 404
    assert response.json()["detail"] == "Notification not found"
