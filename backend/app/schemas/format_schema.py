from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Format Creation Schema
class FormatCreate(BaseModel):
    format_name: str
    text_format: Optional[str] = None
    image_path: Optional[str] = None
    is_default: Optional[bool] = False

# Format Update Schema
class FormatUpdate(BaseModel):
    format_name: Optional[str] = None
    text_format: Optional[str] = None
    image_path: Optional[str] = None
    is_default: Optional[bool] = None

# Format Response Schema
class FormatResponse(BaseModel):
    id: int
    user_id: int
    format_name: str
    text_format: Optional[str] = None
    image_path: Optional[str] = None
    is_default: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Format List Response
class FormatListResponse(BaseModel):
    formats: List[FormatResponse]
    total: int

# Generated Update Schema
class GeneratedUpdate(BaseModel):
    format_id: int
    content: str
    generated_at: datetime