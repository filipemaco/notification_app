import random
import time

from celery import shared_task

from app import schemas
from app.crud import notification as crud_notification
from app.dependencies import db_context


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_notification(self, notification_id: int):
    with db_context() as db:
        crud_notification.update_notification_status(
            db, notification_id, schemas.StatusEnum.in_progress
        )

        time.sleep(2)  # Send request to provider or add to queue

        if not random.choice([0, 0, 0, 1]):
            # Random error in API
            crud_notification.update_notification_status(
                db, notification_id, schemas.StatusEnum.failed
            )
            raise Exception()

        crud_notification.update_notification_status(db, notification_id, schemas.StatusEnum.done)


@shared_task(name="schedule_failed_notifications")
def schedule_failed_notifications():
    with db_context() as db:
        for notification_id in crud_notification.get_stuck_notifications(db):
            send_notification.delay(notification_id)
