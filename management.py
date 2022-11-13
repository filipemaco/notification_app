import json

import typer

from app.database import Base, SessionLocal, engine
from app.models import Notification, User

app = typer.Typer()


@app.command()
def recreate_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@app.command()
def populate_db():
    data = json.loads(open("dummy_data/users.json").read())
    db = SessionLocal()
    for d in data:
        db.add(User(**d))

    data = json.loads(open("dummy_data/notifications.json").read())
    for d in data:
        db.add(Notification(**d))

    db.commit()
    db.close()


if __name__ == "__main__":
    app()
