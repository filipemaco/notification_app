import json
from datetime import datetime, timedelta

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
    one_day_ago = datetime.utcnow() - timedelta(days=1)

    for d in data:
        db.add(Notification(created_at=one_day_ago, **d))

    db.commit()
    db.close()


if __name__ == "__main__":
    app()
