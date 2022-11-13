import logging

from fastapi import FastAPI

from app.database import Base, SessionLocal, engine

logger = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app = FastAPI()

    from app.views import notifications_router, users_router

    app.include_router(users_router)
    app.include_router(notifications_router)

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    logger.info("Drop tables")
    Base.metadata.drop_all(bind=engine)
    logger.info("Creating initial data")
    Base.metadata.create_all(bind=engine)

    import json

    data = json.loads(open("./dummy_data/users.json").read())

    from app.models import User

    db = SessionLocal()
    for d in data:
        db.add(User(**d))
    db.commit()
    db.close()

    logger.info("Initial data created")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)