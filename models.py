from database import Base
from sqlalchemy import Column, Integer, String
import sqlalchemy


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String)
    created_at = Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False)
    
