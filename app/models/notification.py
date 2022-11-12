from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True, index=True)
    status = Column(String(64), nullable=False)
    subject = Column(String(128), nullable=False)
    content = Column(JSONB)
    notification_type = Column(String(64), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="notifications")
