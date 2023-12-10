import datetime as dt

import pytest

from data_cleaner.models import Person, Child
from domain.models import PersonUser
from domain.system import System


class FakeRepository:
    def __init__(self, people: list[PersonUser]):
        self.people = people
        self.children = [child for person in self.people for child in person.children]

    def get_person_by_telephone_number(
            self,
            telephone_number,
            with_children: bool = False
    ) -> PersonUser:
        person = next(filter(lambda x: x.telephone_number == telephone_number, self.people), None)
        return person

    def get_person_by_email(
            self,
            email,
            with_children: bool = False
    ) -> PersonUser:
        person = next(filter(lambda x: x.email == email, self.people), None)
        return person

    def get_oldest_account(self) -> PersonUser:
        account = next(filter(lambda x: x == min(self.people, key=lambda y: y.created_at), self.people), None)
        return account

    def get_accounts_count(self) -> int:
        return len(self.people)

    def group_children_by_age(self) -> list[tuple[int, int]]:
        d = {}
        for child in self.children:
            if child.age not in d:
                d[child.age] = 1
            else:
                d[child.age] += 1
        return sorted(d.items(), key=lambda x: x[0])

    def get_similar_users(self, person: PersonUser) -> list[PersonUser]:
        def get_ages(p):
            return {child.age for child in p.children}
        person_children_ages = get_ages(person)
        res = []
        for p in self.people:
            if p != person and person_children_ages.intersection(get_ages(p)):
                p.children = sorted(p.children, key=lambda x: x.name)
                res.append(p)

        return res


@pytest.fixture
def repository(people):
    return FakeRepository(people)


@pytest.fixture
def people():
    child1 = Child(name="Maria", age=5)
    child2 = Child(name="Peter", age=3)
    child3 = Child(name="John", age=4)
    child4 = Child(name="Paul", age=4)

    anna = Person(
        firstname="Anna",
        telephone_number='123456789',
        email='anna@example.pl',
        password='clandestino',
        role='admin',
        created_at=dt.datetime(2023, 12, 12, 15, 15, 15),
        children=[child4]
    )

    maria = Person(
        firstname="Maria",
        telephone_number='423456789',
        email='an4na@example.pl',
        password='destino',
        role='user',
        created_at=dt.datetime(2023, 8, 12, 15, 15, 15),
        children=[child3, child2, child1]
    )
    return [anna, maria]


@pytest.fixture
def tested_system(repository, people):
    return System(repository, user=people[0])


def test_get_oldest_account_str(tested_system: System):
    s = (
    "name: Maria\n"
    "email_address: an4na@example.pl\n"
    "created_at: 2023-08-12 15:15:15"
    )
    assert tested_system.get_oldest_account_str() == s


def test_get_children_grouped_by_age_str(tested_system: System):
    s = (
        "age: 3, count: 1\n"
        "age: 4, count: 2\n"
        "age: 5, count: 1"
    )
    assert tested_system.get_children_grouped_by_age_str() == s


def test_get_accounts_count_str(tested_system: System):
    assert tested_system.get_accounts_count_str() == "2"


def test_get_children_str(tested_system: System):
    s = "Paul, 4"
    assert tested_system.get_children_str() == s


def test_get_similar_children_str(tested_system: System):
    s = "Maria, 423456789: John, 4; Maria, 5; Peter, 3"
    assert tested_system.get_similar_children_str() == s
