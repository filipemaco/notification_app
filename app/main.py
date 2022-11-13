import os

from fastapi import FastAPI

from celery import Celery

from app.database import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(
        title="Zoe Notification System",
        description="Notification System Description",
        version="0.0.1",
    )

    from app.views import notifications_router, users_router
    app.include_router(users_router)
    app.include_router(notifications_router)

    return app


app = create_app()

celery = Celery(
    __name__,
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND")
)
celery.conf.imports = [
    'app.tasks.notification',
]


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
