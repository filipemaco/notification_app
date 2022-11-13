import random
import time

from celery import shared_task

from app.crud import notification as crud_notification
from app.schemas import StatusEnum
from app.dependencies import db_context


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def send_notification(self, notification_id: int):
    with db_context() as db:
        crud_notification.update_notification_status(db, notification_id, StatusEnum.in_progress.value)

        time.sleep(2)  # Send request to provider or add to queue

        if not random.choice([0, 0, 0, 1]):
            # Random error in API
            crud_notification.update_notification_status(db, notification_id, StatusEnum.failed.value)
            db.commit()
            raise Exception()

        crud_notification.update_notification_status(db, notification_id, StatusEnum.done.value)


@shared_task(name="task_schedule_failed_notifications")
def task_schedule_failed_notifications():
    with db_context() as db:
        for notification_id in crud_notification.get_stuck_notifications(db):
            send_notification.delay(notification_id)
