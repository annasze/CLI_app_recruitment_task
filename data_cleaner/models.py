from dataclasses import dataclass


@dataclass
class Child:
    name: str | None = None
    age: str | None = None


@dataclass
class Person:
    firstname: str | None = None
    telephone_number: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
    created_at: str | None = None
    children: list[Child] | None = None
