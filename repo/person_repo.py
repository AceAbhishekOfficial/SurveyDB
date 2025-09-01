from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from models.person_model import Person
from schemas.person_schema import PersonCreate, PersonUpdate
from typing import List, Optional
from datetime import datetime
from sqlalchemy import func, or_, and_

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


    def get_by_filters(
        self,
        full_name: str | None = None,
        village: str | None = None,
        block: str | None = None,
        district: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ):
        """
        DB-side filtering + pagination.
        Returns (items, total_count).
        Uses substring "includes" semantics (case-insensitive).
        Falls back gracefully if some model attributes are missing.
        """
        q = self.db.query(Person)

        clauses = []

        if full_name:
            # full_name column if present
            fn_attr = getattr(Person, "fullName", None)
            if fn_attr is not None:
                clauses.append(fn_attr.ilike(f"%{full_name}%"))

        if village:
            v_attr = getattr(Person, "village", None)
            if v_attr is not None:
                clauses.append(v_attr.ilike(f"%{village}%"))

        if block:
            b_attr = getattr(Person, "block", None)
            if b_attr is not None:
                clauses.append(b_attr.ilike(f"%{block}%"))

        if district:
            d_attr = getattr(Person, "district", None)
            if d_attr is not None:
                clauses.append(d_attr.ilike(f"%{district}%"))

        # Apply AND across filters, OR only inside full_name matching
        if clauses:
            q = q.filter(and_(*clauses))

        # total count
        total = q.order_by(None).count()

        # pagination
        items = q.offset(offset).limit(limit).all() if limit else q.offset(offset).all()

        return items, total
