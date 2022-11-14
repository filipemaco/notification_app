from fastapi import FastAPI

from app.database import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(
        title="Zoe Notification System",
        description="A notification system for push notification, SMS message and email",
        version="0.0.1",
    )

    from app.celery_utils import create_celery
    app.celery_app = create_celery()

    from app.views import users_router
    app.include_router(users_router)

    from app.views import notifications_router
    app.include_router(notifications_router)

    @app.on_event("startup")
    async def startup_event():
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()
celery = app.celery_app
