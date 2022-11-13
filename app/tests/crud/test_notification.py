from app import schemas
from app.crud import notification as crud_notification
from app.crud import user as crud_user


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


def test_get_notifications(db_session):
    user_id = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=11,
            email="random@gmail.com",
            country_code=22,
            phone_number=333333,
        ),
    ).id

    for _ in range(5):
        crud_notification.create_user_notification(
            db_session,
            schemas.NotificationCreate(
                subject="Text",
                content={"random": "text"},
                notification_type=schemas.NotificationTypeEnum.email.value,
                user_id=user_id,
            ),
        )

    notifications = crud_notification.get_notifications(db_session)

    assert len(notifications) == 5
