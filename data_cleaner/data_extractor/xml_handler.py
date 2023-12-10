from __future__ import annotations

import logging
from pathlib import Path

from .base_handler import Handler
from data_cleaner.models import Child, Person

logger = logging.getLogger(__name__)


class XMLHandler(Handler):
    def handle(self, file_path: Path) -> str:
        if file_path.suffix == ".xml":
            logger.info(f"Handling: {file_path}")
            return self.load(file_path)
        return super().handle(file_path)

    def load(self, file_path):
        import xml.etree.ElementTree as ET

        with open(file_path, "r", encoding='utf-8') as file:
            try:
                data = ET.parse(file).getroot()
                data_length = len(data)
                if data_length > 0:
                    logger.info("Found %d records.", data_length)
            except ET.ParseError as exc:
                logger.warning("Input: %s is invalid. Exception: %s.", file_path, exc)

        return self.add(data)

    def add(self, data):
        num_of_records = len(self._data)
        for user in data:
            person = Person()
            for attr in user:
                if hasattr(person, attr.tag) and attr.tag != 'children':
                    setattr(person, attr.tag, attr.text)
                elif attr.tag == 'children':
                    children = []
                    for child in attr:
                        children.append(Child(**{child_attr.tag: child_attr.text for child_attr in child}))
                    person.children = children
            self._data.append(person)
        logger.info("Added %s records.", len(self._data) - num_of_records)
