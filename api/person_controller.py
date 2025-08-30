from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from service.person_service import PersonService
from schemas.person_schema import PersonCreate, PersonUpdate, PersonResponse
from .auth_controller import get_current_user

router = APIRouter(
    prefix="/persons",
    tags=["person"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/person", response_model=PersonResponse)
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    return PersonService(db).create_person(person)

@router.get("/person/{person_id}", response_model=PersonResponse)
def get_person(person_id: str, db: Session = Depends(get_db)):
    db_person = PersonService(db).get_person(person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.put("/person/{person_id}", response_model=PersonResponse)
def update_person(person_id: str, person_update: PersonUpdate, db: Session = Depends(get_db)):
    db_person = PersonService(db).update_person(person_id, person_update)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.delete("/person/{person_id}", response_model=PersonResponse)
def delete_person(person_id: str, deleted_by: str = Query(...), db: Session = Depends(get_db)):
    db_person = PersonService(db).delete_person(person_id, deleted_by)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.get("/person", response_model=List[PersonResponse])
def get_persons_updated_after(updatedAfter: datetime = 0, db: Session = Depends(get_db)):
    return PersonService(db).get_persons_updated_after(updatedAfter)

@router.post("/persons/bulk", response_model=list[PersonResponse])
def bulk_upsert_persons(persons: list[PersonCreate], db: Session = Depends(get_db)):
    return PersonService(db).bulk_upsert_persons(persons)
