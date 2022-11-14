from app import schemas
from app.crud import user as crud_user
from app.crud import notification as crud_notification


def test_create_user(db_session):
    id = 5423
    email = "random@gmail.com"
    country_code = 22
    phone_number = 333333

    user = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=id, email=email, country_code=country_code, phone_number=phone_number
        ),
    )

    assert user.id == id
    assert user.email == email
    assert user.country_code == country_code
    assert user.phone_number == phone_number


def test_get_user(db_session):
    expected_user = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=2, email="random@gmail.com", country_code=22, phone_number=333333
        ),
    )

    user = crud_user.get_user(db_session, expected_user.id)

    assert user.id == expected_user.id
    assert user.email == expected_user.email
    assert user.country_code == expected_user.country_code
    assert user.phone_number == expected_user.phone_number


def test_get_user_by_email(db_session):
    expected_user = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=2, email="random@gmail.com", country_code=22, phone_number=333333
        ),
    )

    user = crud_user.get_user_by_email(db_session, expected_user.email)

    assert user.id == expected_user.id
    assert user.email == expected_user.email
    assert user.country_code == expected_user.country_code
    assert user.phone_number == expected_user.phone_number

    user = crud_user.get_user_by_email(
        db_session, expected_user.email, expected_user.id
    )

    assert not user


def test_get_user_by_code_and_phone(db_session):
    expected_user = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=2, email="random@gmail.com", country_code=22, phone_number=333333
        ),
    )

    user = crud_user.get_user_by_code_and_phone(
        db_session, expected_user.country_code, expected_user.phone_number
    )

    assert user.id == expected_user.id
    assert user.email == expected_user.email
    assert user.country_code == expected_user.country_code
    assert user.phone_number == expected_user.phone_number

    user = crud_user.get_user_by_code_and_phone(
        db_session,
        expected_user.country_code,
        expected_user.phone_number,
        expected_user.id,
    )

    assert not user


def test_get_users(db_session):
    for i in range(1, 6):
        crud_user.create_user(
            db_session,
            schemas.UserCreate(
                id=i,
                email=f"random{i}@gmail.com",
                country_code=22 + i,
                phone_number=333333 + i,
            ),
        )

    user = crud_user.get_users(db_session)

    assert len(user) == 5


def test_update_user(db_session):
    user_id = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=5423, email="random@gmail.com", country_code=22, phone_number=333333
        ),
    ).id

    user_update = schemas.UserUpdate(
        email="test@gmail.com", country_code=44, phone_number=3222133
    )

    user = crud_user.update_user(db_session, user_id, user_update)

    assert user.id == user_id
    assert user.email == user_update.email
    assert user.country_code == user_update.country_code
    assert user.phone_number == user_update.phone_number


def test_delete_user(db_session):
    user_id = crud_user.create_user(
        db_session,
        schemas.UserCreate(
            id=2, email="random@gmail.com", country_code=22, phone_number=333333
        ),
    ).id

    notification_id = crud_notification.create_user_notification(
        db_session,
        schemas.NotificationCreate(
            subject="Text",
            content={"random": "text"},
            notification_type=schemas.NotificationTypeEnum.email.value,
            user_id=user_id,
        ),
    ).id

    crud_user.delete_user(db_session, user_id)

    user = crud_user.get_user(db_session, user_id)
    notification = crud_notification.get_notification(db_session, notification_id)

    assert not user
    assert not notification
