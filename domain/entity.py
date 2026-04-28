"""Базовая сущность с уникальным кодом-идентификатором."""


class entity:
    """Любой объект предметной области, идентифицируемый целочисленным кодом."""

    def __init__(self, code=0):
        self.setCode(code)

    def setCode(self, value):
        self.__code = value

    def getCode(self):
        return self.__code
