import os

import pytest

os.environ["FASTAPI_CONFIG"] = "testing"  # noqa


@pytest.fixture
def settings():
    from app.config import settings as _settings
    return _settings


@pytest.fixture
def app(settings):
    from app.main import create_app
    return create_app()


@pytest.fixture()
def db_session(app):
    from app.database import Base, SessionLocal, engine

    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(app):
    from fastapi.testclient import TestClient

    yield TestClient(app)
