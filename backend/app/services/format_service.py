from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from ..models.format_model import Format
from ..models.user_model import User
from ..schemas.format_schema import FormatCreate, FormatUpdate

class FormatService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_format(self, format_data: FormatCreate, user: User) -> Format:
        """Create a new format for user"""
        # If this is set as default, unset other defaults
        if format_data.is_default:
            self.db.query(Format).filter(
                Format.user_id == user.id,
                Format.is_default == True
            ).update({"is_default": False})
        
        db_format = Format(
            user_id=user.id,
            format_name=format_data.format_name,
            text_format=format_data.text_format,
            image_path=format_data.image_path,
            is_default=format_data.is_default
        )
        
        self.db.add(db_format)
        self.db.commit()
        self.db.refresh(db_format)
        
        return db_format
    
    def get_user_formats(self, user: User) -> List[Format]:
        """Get all formats for a user"""
        return self.db.query(Format).filter(
            Format.user_id == user.id
        ).order_by(Format.is_default.desc(), Format.created_at.desc()).all()
    
    def get_format_by_id(self, format_id: int, user: User) -> Format:
        """Get a specific format by ID for the user"""
        format_obj = self.db.query(Format).filter(
            Format.id == format_id,
            Format.user_id == user.id
        ).first()
        
        if not format_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Format not found"
            )
        
        return format_obj
    
    def update_format(self, format_id: int, format_data: FormatUpdate, user: User) -> Format:
        """Update a format"""
        format_obj = self.get_format_by_id(format_id, user)
        
        # If setting as default, unset other defaults
        if format_data.is_default:
            self.db.query(Format).filter(
                Format.user_id == user.id,
                Format.id != format_id,
                Format.is_default == True
            ).update({"is_default": False})
        
        update_data = format_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(format_obj, field, value)
        
        self.db.commit()
        self.db.refresh(format_obj)
        
        return format_obj
    
    def delete_format(self, format_id: int, user: User) -> bool:
        """Delete a format"""
        format_obj = self.get_format_by_id(format_id, user)
        
        self.db.delete(format_obj)
        self.db.commit()
        
        return True
    
    def get_default_format(self, user: User) -> Optional[Format]:
        """Get user's default format"""
        return self.db.query(Format).filter(
            Format.user_id == user.id,
            Format.is_default == True
        ).first()
    
    def set_default_format(self, format_id: int, user: User) -> Format:
        """Set a format as default"""
        # Unset all current defaults
        self.db.query(Format).filter(
            Format.user_id == user.id,
            Format.is_default == True
        ).update({"is_default": False})
        
        # Set new default
        format_obj = self.get_format_by_id(format_id, user)
        format_obj.is_default = True
        
        self.db.commit()
        self.db.refresh(format_obj)
        
        return format_obj