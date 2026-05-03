"""Базовая сущность с уникальным кодом-идентификатором."""


class Entity:
    """Любой объект предметной области, идентифицируемый целочисленным кодом."""

    def __init__(self, code=0):
        self.set_code(code)

    def set_code(self, value):
        self.__code = value

    def get_code(self):
        return self.__code
