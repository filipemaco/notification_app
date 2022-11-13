from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class NotificationTypeEnum(str, Enum):
    push = "push"
    sms = "sms"
    email = "email"


class StatusEnum(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"


class NotificationBase(BaseModel):
    subject: str
    content: dict
    notification_type: NotificationTypeEnum
    user_id: int


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: int
    status: StatusEnum
    created_at: datetime

    class Config:
        orm_mode = True
