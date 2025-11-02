from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..core.database import get_db
from ..schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, DailySummary
from ..services.task_service import TaskService
from ..routes.auth_routes import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    task_service = TaskService(db)
    task = task_service.create_task(task_data, current_user)
    return task

@router.get("/", response_model=TaskListResponse)
def get_tasks(
    task_date: Optional[date] = Query(None, description="Filter tasks by date"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user tasks, optionally filtered by date"""
    task_service = TaskService(db)
    tasks = task_service.get_user_tasks(current_user, task_date, limit)
    
    return TaskListResponse(
        tasks=tasks,
        total=len(tasks)
    )

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task by ID"""
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id, current_user)
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task"""
    task_service = TaskService(db)
    task = task_service.update_task(task_id, task_data, current_user)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task"""
    task_service = TaskService(db)
    task_service.delete_task(task_id, current_user)
    return

@router.get("/date-range", response_model=TaskListResponse)
def get_tasks_by_date_range(
    start_date: date = Query(..., description="Start date for task range"),
    end_date: date = Query(..., description="End date for task range"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tasks within a date range"""
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before or equal to end date"
        )
    
    task_service = TaskService(db)
    tasks = task_service.get_tasks_by_date_range(current_user, start_date, end_date)
    
    return TaskListResponse(
        tasks=tasks,
        total=len(tasks)
    )

@router.get("/summary/{summary_date}")
def generate_daily_summary(
    summary_date: date,
    format_template: Optional[str] = Query(None, description="Custom format template"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate daily client update summary"""
    task_service = TaskService(db)
    summary = task_service.generate_daily_summary(current_user, summary_date, format_template)
    
    return {
        "date": summary_date,
        "summary": summary,
        "generated_at": date.today()
    }