import logging

from data_cleaner.models import Person

logger = logging.getLogger(__name__)


def get_validated_dataset(data: list[Person]):
    emails = set()
    telephone_numbers = set()
    validated = []

    for person in data:
        if (person.telephone_number not in telephone_numbers and
                person.email not in emails
        ):
            validated.append(person)
            emails.add(person.email)
            telephone_numbers.add(person.telephone_number)

        else:
            if person.telephone_number in telephone_numbers:
                p = next(filter(lambda x: x.telephone_number == person.telephone_number, validated))
            else:
                p = next(filter(lambda x: x.email == person.email, validated))
            message = "Duplicated record found:\n First: %s\nSecond: %s" % (
                (p.telephone_number, p.email, p.created_at),
                (person.telephone_number, person.email, person.created_at)
            )
            if p.created_at < person.created_at:
                validated.remove(p)
                validated.append(person)
                logger.warning(message + "\nRemoved record created at: %s\n", p.created_at)
            else:
                logger.warning(message + "\nRemoved record created at: %s\n", person.created_at)

    return validated
