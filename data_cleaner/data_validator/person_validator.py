import logging
import re
import datetime as dt

from ..models import Person

logger = logging.getLogger(__name__)


class PersonValidator:
    def __init__(self, unvalidated_person: Person):
        self._person = unvalidated_person
        self.valid = True

        for k, v in self._person.__dict__.items():
            if hasattr(self, "validate_%s" % k):
                getattr(self, "validate_%s" % k)(v)

    def validate_email(self, email: str):
        if email is None:
            logging.warning("Missing email address: %s", self._person)
            self.valid = False
            return
        email.strip(" ")
        pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[\w\d]{1,4}$")
        if re.search(pattern, email) is None:
            logging.warning("Invalid email address: %s", email)
            self.valid = False
        self._person.email = email

    def validate_telephone_number(self, num: str):
        if not num:
            logging.warning("Missing telephone number:\n" + str(self._person))
            self.valid = False
            return
        num = num.lstrip("0")
        num = num.replace(" ", "")
        num.replace("()", "")

        self._person.telephone_number = num[-9:]

    def validate_role(self, role: str):
        role = role.lower()
        if role not in ['admin', 'user']:
            logging.warning("Invalid role: %s", role)
            self.valid = False
        self._person.role = role

    def validate_created_at(self, created_at: str):
        try:
            self._person.created_at = dt.datetime.fromisoformat(created_at)
        except ValueError:
            logging.warning("Invalid created_at format: %s", created_at)
            self.valid = False

    def validate_children(self, children):
        for child in children:
            if not isinstance(child.age, int):
                try:
                    child.age = int(child.age)
                except ValueError:
                    logging.warning("Invalid age: %s", child.age)
                    self.valid = False

    def get_person(self):
        if self.valid:
            return self._person


def get_validated_records(unvalidated_data: list[Person]):
    validated = []

    for record in unvalidated_data:
        person = PersonValidator(record).get_person()
        if person:
            validated.append(person)

    return validated

