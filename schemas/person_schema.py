from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------------------------
# Base Schema (common fields)
# ---------------------------
class PersonBase(BaseModel):
    id: Optional[str] = None  # allow null for new records
    fullName: str
    fatherOrHusbandName: Optional[str] = None
    dateOfBirth: Optional[datetime] = None
    gender: str
    religion: str
    casteCategory: str
    married: bool
    highestEducationLevel: str
    village: str
    block: str
    district: str
    address: str
    mobileNumber: Optional[str] = None
    rationCardHolder: bool
    occupation: str
    createdBy: str
    updatedBy: str

# ---------------------------
# For Create / Update
# ---------------------------
class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    fullName: Optional[str] = None
    fatherOrHusbandName: Optional[str] = None
    dateOfBirth: Optional[datetime] = None
    gender: Optional[str] = None
    religion: Optional[str] = None
    casteCategory: Optional[str] = None
    married: Optional[bool] = None
    highestEducationLevel: Optional[str] = None
    village: Optional[str] = None
    block: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    mobileNumber: Optional[str] = None
    rationCardHolder: Optional[bool] = None
    occupation: Optional[str] = None
    updatedBy: Optional[str] = None

# ---------------------------
# For Response
# ---------------------------
class PersonResponse(PersonBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
    isDeleted: bool
    deltedBy: Optional[str] = None

    class Config:
        orm_mode = True
