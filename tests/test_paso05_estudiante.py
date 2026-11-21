"""Pruebas escritas por el estudiante para el Paso 5 (Pruebas automatizadas desde cero).

Sigue el patrón Arrange -> Act -> Assert usando `paso05_pruebas.calculate_late_fee`:
1. Un caso normal (por ejemplo, 4 días de atraso a tarifa 2.50 -> Decimal("10.00")).
2. Un caso borde con `days_late <= 0` (0 días y días negativos -> Decimal("0.00")).
3. Una prueba que falle si `calculate_late_fee` es sustituida por `calculate_late_fee_buggy`.

Corre `uv run pytest tests/test_paso05_estudiante.py` y `uv run onramp check --paso 5`.
"""

from decimal import Decimal

import pytest

import paso05_pruebas


def test_normal_late_fee() -> None:
    """TODO 1: Verifica el cálculo normal de multa para varios días de atraso."""
    _ = (Decimal, paso05_pruebas)
    pytest.fail("Completa test_normal_late_fee con Arrange, Act y Assert.")


def test_edge_case_zero_or_negative_days() -> None:
    """TODO 2: Verifica que 0 días y días negativos devuelvan Decimal('0.00')."""
    _ = (Decimal, paso05_pruebas)
    pytest.fail("Completa test_edge_case_zero_or_negative_days con días <= 0.")


def test_detects_bug_in_late_fee() -> None:
    """TODO 3: Verifica una regla exacta que la versión con bug no cumple."""
    _ = (Decimal, paso05_pruebas)
    pytest.fail("Completa test_detects_bug_in_late_fee para detectar la versión con bug.")
