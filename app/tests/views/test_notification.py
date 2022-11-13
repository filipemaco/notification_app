from app import schemas
from app.crud import notification as crud_notifications
from app.crud import user as crud_user


def test_get_notifications_ok(client, db_session):
    users = []
    # Create five users
    for i in range(1, 6):
        users.append(
            crud_user.create_user(
                db_session,
                schemas.UserCreate(
                    id=i,
                    email=f"random{i}@gmail.com",
                    country_code=22 + i,
                    phone_number=333333 + i,
                ),
            )
        )

    # Create two notification for each user
    for user in users:
        for _ in range(2):
            crud_notifications.create_user_notification(
                db_session,
                schemas.NotificationCreate(
                    subject="Text",
                    content={"random": "text"},
                    notification_type=schemas.NotificationTypeEnum.email.value,
                    user_id=user.id,
                ),
            )

    response = client.get("/notifications/")

    assert response.status_code == 200
    assert len(response.json()) == 10


def test_create_notification_ok(client, db_session):
    user = schemas.UserCreate(
        id=2, email="random@gmail.com", country_code=22, phone_number=333333
    )
    crud_user.create_user(db_session, user)

    notification = schemas.NotificationCreate(
        subject="Text",
        content={"random": "text"},
        notification_type=schemas.NotificationTypeEnum.sms.value,
        user_id=user.id,
    )

    response = client.post("/notifications/", json=notification.dict())
    content = response.json()

    assert response.status_code == 200
    assert content["status"] == schemas.StatusEnum.new.value
    assert content["subject"] == notification.subject
    assert content["notification_type"] == notification.notification_type
    assert content["user_id"] == user.id


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
    user = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=2, email="random@gmail.com", country_code=22, phone_number=333333
        ),
    )
    notification = crud_notifications.create_user_notification(
        db_session,
        schemas.NotificationCreate(
            subject="Text",
            content={"random": "text"},
            notification_type=schemas.NotificationTypeEnum.email.value,
            user_id=user.id,
        ),
    )

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
