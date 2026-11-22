"""Pruebas escritas por el estudiante para el Paso 5 (Pruebas automatizadas desde cero).

Sigue el patrón Arrange -> Act -> Assert usando `paso05_pruebas.calculate_late_fee`:
1. Un caso normal, con varios días de atraso.
2. Un caso borde, sin atraso.
3. Un tercer caso que elijas después de comparar las versiones con `uv run onramp inspect --paso 5`.

El verificador corre estos tests contra la función correcta y contra dos versiones con un bug.
Deben pasar con la primera y fallar con cada una de las otras dos.

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
    """TODO 2: Verifica qué pasa cuando no hay atraso."""
    _ = (Decimal, paso05_pruebas)
    pytest.fail("Completa test_edge_case_zero_or_negative_days.")


def test_detects_bug_in_late_fee() -> None:
    """TODO 3: Verifica un caso donde alguna versión con un bug se equivoca."""
    _ = (Decimal, paso05_pruebas)
    pytest.fail("Completa test_detects_bug_in_late_fee.")
