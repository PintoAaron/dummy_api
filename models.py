from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy
from uuid import uuid4
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String)
    created_at = Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False)
    
    requests = relationship("Requests", back_populates="user")

class Requests(Base):
    __tablename__ = "requests"
    order_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    food = Column(String, nullable=False)
    created_at = Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False)

    user = relationship("User", back_populates="requests")
