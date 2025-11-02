from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Registration Schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User Response Schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# User Update Schema
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    
# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None