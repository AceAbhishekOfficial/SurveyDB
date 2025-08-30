from sqlalchemy.orm import Session
from repo.person_repo import PersonRepository
from schemas.person_schema import PersonCreate, PersonUpdate
from models.person_model import Person
from typing import List, Optional
from datetime import datetime

class PersonService:
    def __init__(self, db: Session):
        self.repo = PersonRepository(db)

    def create_person(self, person: PersonCreate) -> Person:
        return self.repo.create(person)

    def get_person(self, person_id: str) -> Optional[Person]:
        return self.repo.get_by_id(person_id)

    def update_person(self, person_id: str, person_update: PersonUpdate) -> Optional[Person]:
        return self.repo.update(person_id, person_update)

    def delete_person(self, person_id: str, deleted_by: str) -> Optional[Person]:
        return self.repo.delete(person_id, deleted_by)

    def get_persons_updated_after(self, timestamp: datetime) -> List[Person]:
        return self.repo.get_updated_after(timestamp)
