from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..schemas.format_schema import FormatCreate, FormatUpdate, FormatResponse, FormatListResponse
from ..services.format_service import FormatService
from ..routes.auth_routes import get_current_user

router = APIRouter(prefix="/formats", tags=["Formats"])

@router.post("/", response_model=FormatResponse, status_code=status.HTTP_201_CREATED)
def create_format(
    format_data: FormatCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new format"""
    format_service = FormatService(db)
    format_obj = format_service.create_format(format_data, current_user)
    return format_obj

@router.get("/", response_model=FormatListResponse)
def get_formats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user formats"""
    format_service = FormatService(db)
    formats = format_service.get_user_formats(current_user)
    
    return FormatListResponse(
        formats=formats,
        total=len(formats)
    )

@router.get("/{format_id}", response_model=FormatResponse)
def get_format(
    format_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific format by ID"""
    format_service = FormatService(db)
    format_obj = format_service.get_format_by_id(format_id, current_user)
    return format_obj

@router.put("/{format_id}", response_model=FormatResponse)
def update_format(
    format_id: int,
    format_data: FormatUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a format"""
    format_service = FormatService(db)
    format_obj = format_service.update_format(format_id, format_data, current_user)
    return format_obj

@router.delete("/{format_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_format(
    format_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a format"""
    format_service = FormatService(db)
    format_service.delete_format(format_id, current_user)
    return

@router.get("/default/current", response_model=FormatResponse)
def get_default_format(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's default format"""
    format_service = FormatService(db)
    default_format = format_service.get_default_format(current_user)
    
    if not default_format:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No default format found"
        )
    
    return default_format

@router.post("/{format_id}/set-default", response_model=FormatResponse)
def set_default_format(
    format_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set a format as default"""
    format_service = FormatService(db)
    format_obj = format_service.set_default_format(format_id, current_user)
    return format_obj