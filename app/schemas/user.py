from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class GoogleLoginRequest(BaseModel):
    credential: str


class StudentProfileUpdate(BaseModel):
    # Personal information
    name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    location: Optional[str] = None

    # Academic information
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    semester: Optional[int] = None
    cgpa: Optional[float] = None

    # Career preferences
    preferred_roles: Optional[str] = None
    preferred_industries: Optional[str] = None
    preferred_work_locations: Optional[str] = None