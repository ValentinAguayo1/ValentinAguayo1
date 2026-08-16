from utils import calculate_rank, clamp, format_number, percentage


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


def test_calculate_rank_low_activity_is_c():
    letter, percentile = calculate_rank(
        commits=46,
        pull_requests=0,
        issues=0,
        stars=0,
        followers=5,
    )
    assert letter in {"C", "C+"}
    assert percentile > 80


def test_calculate_rank_high_activity_is_strong():
    letter, percentile = calculate_rank(
        commits=2000,
        pull_requests=200,
        issues=80,
        stars=400,
        followers=300,
    )
    assert letter in {"S", "A+", "A"}
    assert percentile < 25
