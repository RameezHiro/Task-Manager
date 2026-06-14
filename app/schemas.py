from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

# --- Enums ---
class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in-progress"
    done = "done"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# --- User Schemas ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Task Schemas ---
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.todo
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: StatusEnum
    priority: PriorityEnum
    due_date: Optional[datetime]
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class TaskStatusUpdate(BaseModel):
    status: StatusEnum