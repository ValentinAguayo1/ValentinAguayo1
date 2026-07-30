from datetime import datetime, timezone


def format_number(value: int) -> str:
    """
    Formatea un número con separadores de miles.
    """
    return f"{value:,}"


def current_timestamp() -> str:
    """
    Devuelve la fecha y hora actual en formato UTC.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    Limita un valor entre un mínimo y un máximo.
    """
    return max(minimum, min(value, maximum))


def percentage(value: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((value / total) * 100, 1)