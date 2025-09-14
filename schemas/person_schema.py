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
    age: Optional[str] = None
    gender: str
    religion: str
    casteCategory: str
    cast:str
    married: str
    highestEducationLevel: str
    village: str
    block: str
    district: str
    houseNo: str
    address: str
    mobileNumber: Optional[str] = None
    rationCardHolder: bool
    adhaarCardNumber: Optional[str] = None
    occupation: str
    createdBy: str
    updatedBy: str
    isDeleted: Optional[bool] = False

# ---------------------------
# For Create / Update
# ---------------------------
class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    fullName: Optional[str] = None
    fatherOrHusbandName: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    religion: Optional[str] = None
    casteCategory: Optional[str] = None
    cast: Optional[str] = None
    married: Optional[str] = None
    highestEducationLevel: Optional[str] = None
    village: Optional[str] = None
    block: Optional[str] = None
    district: Optional[str] = None
    houseNo: Optional[str] = None
    adhaarCardNumber: Optional[str] = None
    address: Optional[str] = None
    mobileNumber: Optional[str] = None
    rationCardHolder: Optional[bool] = None
    occupation: Optional[str] = None
    updatedBy: Optional[str] = None
    isDeleted: Optional[bool] = False

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

class PaginatedPersons(BaseModel):
    data: List[PersonResponse]
    page: int
    size: int
    totalPages: int
    totalItems: int
    hasNext: bool
    hasPrevious: bool
