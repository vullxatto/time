"""Общие утилиты доменного слоя (без зависимостей от веба и сериализации)."""


def to_int(value, default=0):
    """Безопасное приведение к int для полей модели."""
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return default
