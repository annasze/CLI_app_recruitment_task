import datetime as dt

from sqlalchemy import String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from domain import models
from config import SQLITE_DB_NAME


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "Person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(40))
    role: Mapped[str] = mapped_column(String(5))
    created_at: Mapped[dt.datetime] = mapped_column(DateTime)
    telephone_number: Mapped[str] = mapped_column(String(9), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    children: Mapped[list["Child"]] = relationship()


class Child(Base):
    __tablename__ = "Child"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    age: Mapped[int] = mapped_column(Integer)

    person_id: Mapped[int] = mapped_column(ForeignKey("Person.id"))
    person: Mapped["Person"] = relationship(back_populates="children")


def create_sqlite_db(data: list[models.PersonUser], db_name: str = SQLITE_DB_NAME):
    engine = create_engine(rf"sqlite:///{db_name}")
    Base.metadata.create_all(engine)

    sqlalchemy_models = convert_to_sqlalchemy_models(data)
    with Session(engine) as session:
        session.add_all(sqlalchemy_models)
        session.commit()


def convert_to_sqlalchemy_models(data: list[models.PersonUser]):
    sqlalchemy_models = []
    for person in data:
        children = [Child(age=child.age, name=child.name) for child in person.children]
        p = Person(
            firstname=person.firstname,
            role=person.role,
            created_at=person.created_at,
            telephone_number=person.telephone_number,
            email=person.email,
            password=person.password,
        )
        p.children = children
        sqlalchemy_models.append(p)

    return sqlalchemy_models


