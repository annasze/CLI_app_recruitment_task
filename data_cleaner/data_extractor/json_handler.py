from __future__ import annotations

import logging
from pathlib import Path

from .base_handler import Handler
from data_cleaner.models import Child, Person

logger = logging.getLogger(__name__)


class JsonHandler(Handler):
    def handle(self, file_path: Path) -> str:
        if file_path.suffix == ".json":
            logger.info(f"Handling: {file_path}")
            return self.load(file_path)
        return super().handle(file_path)

    def load(self, file_path):
        import json

        with open(file_path, "r", encoding='utf-8') as file:
            try:
                data = json.load(file)
                data_length = len(data)
                if data_length > 0:
                    logger.info("Found %d records.", data_length)
                    return self.add(data)
                logger.warning("Input: %s contained no data.", file_path)
            except json.decoder.JSONDecodeError as exc:
                logger.warning("Input: %s is invalid. Exception: %s.", file_path, exc)

    def add(self, data):
        num_of_records = len(self._data)
        for person_data in data:
            person = Person()
            for key, value in person_data.items():
                if isinstance(value, str) and hasattr(person, key):
                    setattr(person, key, value)
                elif isinstance(value, list) and hasattr(person, key):
                    setattr(person, key, [Child(**child) for child in value])
            self._data.append(person)
        logger.info("Added %s records.", len(self._data) - num_of_records)

