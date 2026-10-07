from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=3, max_length=30)
    department: str = Field(min_length=1, max_length=100)
    designation: str = Field(min_length=1, max_length=100)
    salary: float = Field(gt=0)
    status: str = Field(min_length=1, max_length=50)
    joining_date: date

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=3, max_length=30)
    department: Optional[str] = Field(default=None, min_length=1, max_length=100)
    designation: Optional[str] = Field(default=None, min_length=1, max_length=100)
    salary: Optional[float] = Field(default=None, gt=0)
    status: Optional[str] = Field(default=None, min_length=1, max_length=50)
    joining_date: Optional[date] = None

class EmployeeResponse(EmployeeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
