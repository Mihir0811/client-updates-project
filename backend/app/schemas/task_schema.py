from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

# Task Creation Schema
class TaskCreate(BaseModel):
    task_title: str
    task_desc: Optional[str] = None
    date: date

# Task Update Schema
class TaskUpdate(BaseModel):
    task_title: Optional[str] = None
    task_desc: Optional[str] = None
    date: Optional[date] = None

# Task Response Schema
class TaskResponse(BaseModel):
    id: int
    user_id: int
    task_title: str
    task_desc: Optional[str] = None
    date: date
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Task List Response
class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int

# Daily Summary Schema
class DailySummary(BaseModel):
    date: date
    tasks: List[TaskResponse]
    summary_text: Optional[str] = None