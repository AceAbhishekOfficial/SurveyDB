from sqlalchemy.orm import Session
from models.person_model import Person
from schemas.person_schema import PersonCreate, PersonUpdate
from typing import List, Optional
from datetime import datetime

class PersonRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, person: PersonCreate) -> Person:
        db_person = Person(**person.dict())
        self.db.add(db_person)
        self.db.commit()
        self.db.refresh(db_person)
        return db_person

    def get_by_id(self, person_id: str) -> Optional[Person]:
        return self.db.query(Person).filter(Person.id == person_id).first()

    def update(self, person_id: str, person_update: PersonUpdate) -> Optional[Person]:
        db_person = self.get_by_id(person_id)
        if not db_person:
            return None
        for key, value in person_update.dict(exclude_unset=True).items():
            setattr(db_person, key, value)
        db_person.updatedAt = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_person)
        return db_person

    def delete(self, person_id: str, deleted_by: str) -> Optional[Person]:
        db_person = self.get_by_id(person_id)
        if not db_person:
            return None
        db_person.isDeleted = True
        db_person.deltedBy = deleted_by
        db_person.updatedAt = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_person)
        return db_person

    def get_updated_after(self, timestamp: datetime) -> List[Person]:
        return self.db.query(Person).filter(Person.updatedAt > timestamp, Person.isDeleted == False).all()
