"""Базовая коллекция сущностей с операциями поиска и генерации новых кодов."""

from domain.entity import entity


class entityList:
    """Список однородных сущностей; обеспечивает уникальность кодов."""

    def __init__(self):
        self.__list = []

    def clear(self):
        self.__list = []

    def findByCode(self, code):
        """Возвращает сущность с заданным кодом или None."""
        for item in self.__list:
            if item.getCode() == code:
                return item
        return None

    def getNewCode(self):
        """Возвращает следующий свободный код (max + 1) или 1, если список пуст."""
        codes = self.getCodes()
        return max(codes) + 1 if codes else 1

    def getCodes(self):
        return [s.getCode() for s in self.__list]

    def getItems(self):
        return self.__list.copy()

    def appendItem(self, value):
        self.__list.append(value)

    def removeItem(self, value):
        if isinstance(value, entity):
            if value in self.__list:
                self.__list.remove(value)
        elif isinstance(value, int):
            obj = self.findByCode(value)
            if obj is not None:
                self.__list.remove(obj)
