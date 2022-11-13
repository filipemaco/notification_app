from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True, index=True)
    status = Column(String(64), nullable=False)
    subject = Column(String(128), nullable=False)
    content = Column(JSONB, nullable=False)
    notification_type = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="notifications")
