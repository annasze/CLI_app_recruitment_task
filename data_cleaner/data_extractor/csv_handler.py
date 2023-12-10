from __future__ import annotations

import logging
import re
from pathlib import Path

from .base_handler import Handler
from data_cleaner.models import Child, Person

logger = logging.getLogger(__name__)


class CSVHandler(Handler):
    def handle(self, file_path: Path) -> str:
        if file_path.suffix == ".csv":
            logger.info(f"Handling: {file_path}")
            return self.load(file_path)
        return super().handle(file_path)

    def load(self, file_path):
        import csv

        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            data = csv.DictReader(csv_file, delimiter=';')
            data = list(data)
            data_length = len(data)
            if data_length > 0:
                logger.info("Found %d records.", data_length)
                return self.add(data)
            logger.warning("Input: %s contained no data.", file_path)

    def add(self, data):
        num_of_records = len(self._data)
        for person_data in data:
            person = Person(**{attr: value for attr, value in person_data.items() if hasattr(Person, attr)})
            person.children = []

            if person_data.get('children'):
                children = person_data['children'].split(",")
                for child in children:
                    name = re.findall('[^\W\d_]+', child)
                    age = re.findall('\d+', child)
                    if len(name) != 1 or len(age) != 1:
                        logger.warning("Invalid child data: %s.", child)
                        break
                    person.children.append(Child(name[0], age[0]))
            self._data.append(person)
        logger.info("Added %s records.", len(self._data) - num_of_records)
