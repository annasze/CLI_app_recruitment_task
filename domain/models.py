from typing import Protocol, runtime_checkable
import datetime as dt


@runtime_checkable
class Child(Protocol):
    name: str
    age: int


@runtime_checkable
class PersonUser(Protocol):
    firstname: str
    telephone_number: str
    email: str
    password: str
    role: str
    created_at: dt.datetime
    children: list[Child]
