from fastapi import FastAPI

from app.database import Base, engine


def create_app() -> FastAPI:
    app = FastAPI()

    from app.views import notifications_router, users_router

    app.include_router(users_router)
    app.include_router(notifications_router)

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
