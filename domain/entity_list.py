"""Базовая коллекция сущностей с операциями поиска и генерации новых кодов."""

from domain.entity import Entity


class EntityList:
    """Список однородных сущностей; обеспечивает уникальность кодов."""

    def __init__(self):
        self.__list = []

    def clear(self):
        self.__list = []

    def find_by_code(self, code):
        """Возвращает сущность с заданным кодом или None."""
        for item in self.__list:
            if item.get_code() == code:
                return item
        return None

    def get_new_code(self):
        """Возвращает следующий свободный код (max + 1) или 1, если список пуст."""
        codes = self.get_codes()
        return max(codes) + 1 if codes else 1

    def get_codes(self):
        return [s.get_code() for s in self.__list]

    def get_items(self):
        return self.__list.copy()

    def append_item(self, value):
        self.__list.append(value)

    def remove_item(self, value):
        if isinstance(value, Entity):
            if value in self.__list:
                self.__list.remove(value)
        elif isinstance(value, int):
            obj = self.find_by_code(value)
            if obj is not None:
                self.__list.remove(obj)
