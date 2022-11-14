from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=False)
    email = Column(String(128), unique=True, nullable=False)
    country_code = Column(Integer, nullable=False)
    phone_number = Column(Integer, nullable=False)

    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    def __str__(self):
        return self.id
