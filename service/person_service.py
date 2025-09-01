from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from repo.person_repo import PersonRepository
from schemas.person_schema import PersonCreate, PersonUpdate
from models.person_model import Person
from typing import List, Optional
from datetime import datetime
import uuid

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

    def bulk_upsert_persons(self, persons: list[PersonCreate]):
        results = []
        for p in persons:
            if not getattr(p, "id", None):
               result = self.repo.create(p)
               results.append(result)

            else:  # ➝ update existing
                result = self.repo.update(p.id, p)
                results.append(result)
        return results

    def get_persons_by_filters(
        self,
        full_name: Optional[str] = None,
        village: Optional[str] = None,
        block: Optional[str] = None,
        district: Optional[str] = None,
        page: int = 1,
        size: int = 20
    ) -> tuple[list[Person], int]:
        """
        DB-side filtering + pagination.
        Returns (items, total_count).

        Preference order:
        1) If repo implements get_by_filters(...) use it.
        2) Else build a SQLAlchemy query against the repo's DB session (preferred).
        3) Fallback to in-memory filtering (only if repo lacks a DB/session).
        """
        offset = max(page - 1, 0) * size

        # # 1) Repo-provided efficient method
        # if hasattr(self.repo, "get_by_filters"):
        return self.repo.get_by_filters(
            full_name=full_name,
            village=village,
            block=block,
            district=district,
            offset=offset,
            limit=size
        )
        #     )

        # # 2) Try to run a DB-side query using repository's session (PersonRepository should expose .db)
        # db_session = getattr(self.repo, "db", None)
        # if db_session is not None:
        #     q = db_session.query(Person)
        #     clauses = []

        #     if full_name:
        #         pattern = f"%{full_name}%"
        #         fn_attr = getattr(Person, "full_name", None)
        #         if fn_attr is not None:
        #             clauses.append(fn_attr.ilike(pattern))

        #         first_attr = getattr(Person, "first_name", None)
        #         last_attr = getattr(Person, "last_name", None)
        #         if first_attr is not None and last_attr is not None:
        #             name_concat = func.concat(func.coalesce(first_attr, ''), ' ', func.coalesce(last_attr, ''))
        #             clauses.append(name_concat.ilike(pattern))

        #     if village:
        #         v_attr = getattr(Person, "village", None)
        #         if v_attr is not None:
        #             clauses.append(v_attr.ilike(f"%{village}%"))

        #     if block:
        #         b_attr = getattr(Person, "block", None)
        #         if b_attr is not None:
        #             clauses.append(b_attr.ilike(f"%{block}%"))

        #     if district:
        #         d_attr = getattr(Person, "district", None)
        #         if d_attr is not None:
        #             clauses.append(d_attr.ilike(f"%{district}%"))

        #     if clauses:
        #         q = q.filter(or_(*clauses)) if len(clauses) > 1 else q.filter(clauses[0])

        #     total = q.order_by(None).count()
        #     items = q.offset(offset).limit(size).all() if size else q.offset(offset).all()
        #     return items, total

        # # 3) Fallback to in-memory filtering (inefficient)
        # all_items: List[Person] = self.repo.get_all()

        # def matches(p: Person) -> bool:
        #     if full_name:
        #         val = (getattr(p, "full_name", None) or "") or \
        #               (" ".join(filter(None, [getattr(p, "first_name", ""), getattr(p, "last_name", "")]))).strip()
        #         if full_name.lower() not in val.lower():
        #             return False
        #     if village and village.lower() not in (getattr(p, "village", "") or "").lower():
        #         return False
        #     if block and block.lower() not in (getattr(p, "block", "") or "").lower():
        #         return False
        #     if district and district.lower() not in (getattr(p, "district", "") or "").lower():
        #         return False
        #     return True

        # filtered = [p for p in all_items if matches(p)]
        # total = len(filtered)
        # paged = filtered[offset: offset + size] if size else filtered[offset:]
        # return paged, total