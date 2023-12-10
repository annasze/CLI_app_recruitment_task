from typing import Protocol

from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy.sql.functions import count

from adapters.orm import Person, Child
from domain.models import PersonUser
from config import SQLITE_DB_NAME


class Repository(Protocol):
    def get_person_by_telephone_number(
            self,
            telephone_number,
            with_children: bool = False
    ) -> PersonUser:
        ...

    def get_person_by_email(
            self,
            email,
            with_children: bool = False
    ) -> PersonUser:
        ...

    def get_oldest_account(self) -> PersonUser:
        ...

    def get_accounts_count(self) -> int:
        ...

    def group_children_by_age(self) -> list[tuple[int, int]]:
        ...

    def get_similar_users(self, person: PersonUser) -> list[PersonUser]:
        ...


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(rf"sqlite:///{SQLITE_DB_NAME}")
)


class SQLAlchemyRepository:
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY) -> None:
        self.session = session_factory()

    def get_person_by_telephone_number(
            self,
            telephone_number,
            with_children: bool = False
    ) -> Person:
        query = self.session.query(Person).filter(
            Person.telephone_number == telephone_number
        )
        if with_children:
            query = query.options(
                joinedload(Person.children)
            ).join(Child).order_by(Child.name)

        return query.first()

    def get_person_by_email(
            self,
            email,
            with_children: bool = False
    ) -> Person:
        query = self.session.query(Person).filter(
            Person.email == email
        )
        if with_children:
            query = query.options(
                joinedload(Person.children)
            ).join(Child).order_by(Child.name)

        return query.first()

    def get_oldest_account(self) -> Person:
        return self.session.query(Person).order_by(Person.created_at).first()

    def get_accounts_count(self) -> int:
        return self.session.query(Person).count()

    def group_children_by_age(self) -> list[tuple[int, int]]:
        return self.session.query(
            Child.age, count(Child.age)
        ).group_by(Child.age).order_by(Child.age).all()

    def get_similar_users(self, person: Person) -> list[Person]:
        ages = {child.age for child in person.children}
        return (
            self.session.query(Person).join(Child).filter(
                Child.age.in_(ages)
            ).options(joinedload(Person.children)).order_by(Child.name).all()
        )
