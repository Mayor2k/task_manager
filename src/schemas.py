from typing import List, Optional, Union
from datetime import date
from pydantic import BaseModel, Field
import enum
from datetime import datetime

class Genders(str, enum.Enum):
    male = "male"
    female = "female"
    
class TaskBase(BaseModel):
    user_id: int
    description: str
    
    class Config:
        orm_mode = True
        
class Task(TaskBase):
    id: int
    created_at: datetime
    
class UserBase(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Genders] = None
    
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: int
    tasks: List[Task]
