from app import schemas
from app.crud import user as crud_user
from app.tests.utils import create_notification_factory, create_user_factory


def test_create_user_ok(client, db_session):
    data = {
        "id": 3123,
        "email": "random@gmai.com",
        "country_code": 22,
        "phone_number": 123321333,
    }

    response = client.post("/users/", json=data)
    content = response.json()
    user = crud_user.get_user(db_session, data["id"])

    assert response.status_code == 200
    assert data["id"] == content["id"] == user.id
    assert data["email"] == content["email"] == user.email
    assert data["country_code"] == content["country_code"] == user.country_code
    assert data["phone_number"] == content["phone_number"] == user.phone_number


def test_create_duplicate_user_failed(client, db_session):
    user = schemas.UserCreate(
        id=2, email="random@gmail.com", country_code=22, phone_number=333333
    )
    crud_user.create_user(db_session, user)

    response = client.post("/users/", json=user.dict())

    assert response.status_code == 400
    assert response.json()["detail"] == "User ID already registered"


def test_create_duplicate_user_email_failed(client, db_session):
    user = schemas.UserCreate(
        id=2, email="random@gmail.com", country_code=22, phone_number=333333
    )
    crud_user.create_user(db_session, user)
    user.id = 3

    response = client.post("/users/", json=user.dict())

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_create_duplicate_user_phone_number_failed(client, db_session):
    user = schemas.UserCreate(
        id=2, email="random@gmail.com", country_code=22, phone_number=333333
    )
    crud_user.create_user(db_session, user)
    user.id, user.email = 3, "random2@gmail.com"

    response = client.post("/users/", json=user.dict())

    assert response.status_code == 400
    assert response.json()["detail"] == "Phone number already registered"


def test_get_users_ok(client, db_session):
    create_user_factory(db_session)
    create_user_factory(
        db=db_session,
        id=2,
        email="text@gmail.com",
        country_code=333,
        phone_number=4444444,
    )

    response = client.get("/users/")

    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get("/users/?skip=0&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/users/?skip=1&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/users/?skip=2&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_user_ok(client, db_session):
    user = create_user_factory(db_session)
    notification = create_notification_factory(db=db_session, user_id=user.id)

    response = client.get(f"/users/{user.id}")
    content = response.json()
    notifications = content.pop("notifications")

    assert response.status_code == 200
    assert content["id"] == user.id
    assert content["email"] == user.email
    assert notifications[0]["status"] == schemas.StatusEnum.new.value
    assert notifications[0]["subject"] == notification.subject
    assert notifications[0]["notification_type"] == notification.notification_type


def test_get_nonexistent_user_failed(client, db_session):
    response = client.get("/users/2")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_ok(client, db_session):
    user = create_user_factory(db_session)

    response = client.delete(f"/users/{user.id}")

    assert response.status_code == 200


def test_delete_user_failed(client, db_session):
    response = client.delete("/users/2")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user_ok(client, db_session):
    user = create_user_factory(db_session)

    user_update = schemas.UserUpdate(
        email="test@gmail.com", country_code=22, phone_number=3222133
    )
    response = client.put(f"/users/{user.id}", json=user_update.dict())

    db_session.refresh(user)

    assert response.status_code == 200
    assert user.email == user_update.email
    assert user.country_code == user_update.country_code
    assert user.phone_number == user_update.phone_number


def test_update_nonexistent_user_failed(client, db_session):
    user = schemas.UserUpdate(
        email="test@gmail.com", country_code=22, phone_number=333333
    )

    response = client.put("/users/1", json=user.dict())

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_duplicate_user_email_failed(client, db_session):
    create_user_factory(db_session, email="random@gmail.com")

    user_id = create_user_factory(
        db=db_session,
        id=2,
        email="text@gmail.com",
        country_code=333,
        phone_number=4444444,
    ).id

    user_update = schemas.UserUpdate(
        email="random@gmail.com", country_code=333, phone_number=4444444
    )
    response = client.put(f"/users/{user_id}", json=user_update.dict())

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_update_duplicate_user_phone_number_failed(client, db_session):
    create_user_factory(db_session, country_code=22, phone_number=333333)

    user_id = create_user_factory(
        db=db_session,
        id=2,
        email="text@gmail.com",
        country_code=333,
        phone_number=4444444,
    ).id

    user_update = schemas.UserUpdate(
        email="text@gmail.com", country_code=22, phone_number=333333
    )
    response = client.put(f"/users/{user_id}", json=user_update.dict())

    assert response.status_code == 400
    assert response.json()["detail"] == "Phone number already registered"
