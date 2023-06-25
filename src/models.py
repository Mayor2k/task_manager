from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from sqlalchemy.sql import func
import enum

class Genders(str, enum.Enum):
    male = "male"
    female = "female"
    
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    #link task with user
    user = relationship("User", back_populates="tasks", lazy='joined')
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"Task №{self.id}"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    gender = Column(Enum(Genders), nullable=False)
    #show tasks list, related with this user
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan", lazy='subquery')
    
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
