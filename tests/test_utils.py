from utils import clamp, format_number, percentage


def test_format_number():
    """Verifica el formato de separadores de miles."""
    assert format_number(1000) == "1,000"
    assert format_number(1000000) == "1,000,000"
    assert format_number(500) == "500"


def test_clamp():
    """Verifica que el valor no sobrepase el mínimo ni el máximo."""
    # Dentro del rango (no cambia)
    assert clamp(5, 0, 10) == 5
    # Por debajo del mínimo (se ajusta al mínimo)
    assert clamp(-5, 0, 10) == 0
    # Por encima del máximo (se ajusta al máximo)
    assert clamp(15, 0, 10) == 10


def test_percentage_normal():
    """Verifica el cálculo correcto del porcentaje."""
    assert percentage(50, 100) == 50.0
    assert percentage(1, 3) == 33.3  # Si usas round() a 1 decimal


def test_percentage_division_por_cero():
    """Verifica que no colapse si el total es cero."""
    assert percentage(10, 0) == 0.0
