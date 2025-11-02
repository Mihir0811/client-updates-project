from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date
from ..models.task_model import Task
from ..models.user_model import User
from ..schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from ..utils.helpers import generate_client_update

class TaskService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_task(self, task_data: TaskCreate, user: User) -> Task:
        """Create a new task for user"""
        db_task = Task(
            user_id=user.id,
            task_title=task_data.task_title,
            task_desc=task_data.task_desc,
            date=task_data.date
        )
        
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        return db_task
    
    def get_user_tasks(self, user: User, task_date: Optional[date] = None, limit: int = 100) -> List[Task]:
        """Get tasks for a user, optionally filtered by date"""
        query = self.db.query(Task).filter(Task.user_id == user.id)
        
        if task_date:
            query = query.filter(Task.date == task_date)
        
        return query.order_by(Task.date.desc(), Task.created_at.desc()).limit(limit).all()
    
    def get_task_by_id(self, task_id: int, user: User) -> Task:
        """Get a specific task by ID for the user"""
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user.id
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return task
    
    def update_task(self, task_id: int, task_data: TaskUpdate, user: User) -> Task:
        """Update a task"""
        task = self.get_task_by_id(task_id, user)
        
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def delete_task(self, task_id: int, user: User) -> bool:
        """Delete a task"""
        task = self.get_task_by_id(task_id, user)
        
        self.db.delete(task)
        self.db.commit()
        
        return True
    
    def get_tasks_by_date_range(self, user: User, start_date: date, end_date: date) -> List[Task]:
        """Get tasks within a date range"""
        return self.db.query(Task).filter(
            Task.user_id == user.id,
            Task.date >= start_date,
            Task.date <= end_date
        ).order_by(Task.date.desc(), Task.created_at.desc()).all()
    
    def generate_daily_summary(self, user: User, summary_date: date, format_template: str = None) -> str:
        """Generate client update summary for a specific date"""
        tasks = self.get_user_tasks(user, task_date=summary_date)
        
        if not tasks:
            return f"No tasks completed on {summary_date.strftime('%Y-%m-%d')}"
        
        # Convert to TaskResponse objects for the helper function
        task_responses = [TaskResponse.from_orm(task) for task in tasks]
        
        return generate_client_update(task_responses, format_template)