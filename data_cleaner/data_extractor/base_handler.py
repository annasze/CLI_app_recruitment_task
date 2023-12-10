from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)


class Handler(ABC):
    _next_handler: Handler = None
    _data = []

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler

        return handler

    @abstractmethod
    def handle(self, file_path: Path) -> str:
        if self._next_handler:
            return self._next_handler.handle(file_path)
        logger.warning("No handler for %s found.", file_path)

    def get_data(self):
        return self._data

