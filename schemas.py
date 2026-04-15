from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# To wysyła Android przy rejestracji
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str = Field(..., min_length=8)
    avatar_url: str | None = None

class UserLoginRequest(BaseModel):
    username: str
    password: str

# To wysyła Serwer do Androida (nigdy nie wysyłamy hasła!)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    created_at: datetime
    avatar_url: str | None
    
    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"