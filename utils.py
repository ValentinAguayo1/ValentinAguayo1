from datetime import datetime


def format_number(value: int) -> str:
    """
    Formatea un número con separadores de miles.
    """
    return f"{value:,}"


def current_timestamp() -> str:
    """
    Devuelve la fecha y hora actual en formato UTC.
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    Limita un valor entre un mínimo y un máximo.
    """
    return max(minimum, min(value, maximum))


def percentage(value: int, total: int) -> float:
    """
    Calcula un porcentaje evitando divisiones por cero.
    """
    if total == 0:
        return 0.0
    return (value / total) * 100