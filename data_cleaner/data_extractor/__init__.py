from .base_handler import Handler
from .json_handler import JsonHandler
from .csv_handler import CSVHandler
from .xml_handler import XMLHandler


def get_handler():
    json_handler = JsonHandler()
    csv_handler = CSVHandler()
    xml_handler = XMLHandler()

    json_handler.set_next(csv_handler).set_next(xml_handler)

    return json_handler