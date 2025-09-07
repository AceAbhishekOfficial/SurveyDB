from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from database import Base
import uuid

class Person(Base):
    __tablename__ = "persons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fullName = Column(String(100), nullable=False)
    fatherOrHusbandName = Column(String(100), nullable=True)
    gender = Column(String(10), nullable=False)
    religion = Column(String(50), nullable=False)
    casteCategory = Column(String(50), nullable=False)
    cast = Column(String(50), nullable=False)
    married = Column(Boolean, nullable=False)
    highestEducationLevel = Column(String(50), nullable=False)
    village = Column(String(100), nullable=False)
    block = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    houseNo = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    mobileNumber = Column(String(20), nullable=True)
    rationCardHolder = Column(Boolean, nullable=False)
    occupation = Column(String(100), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    createdBy = Column(String(50), nullable=False)
    updatedBy = Column(String(50), nullable=False)
    isDeleted = Column(Boolean, default=False)
    deltedBy = Column(String(50), nullable=True)
