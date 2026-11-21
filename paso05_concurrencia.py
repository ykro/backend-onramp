"""Paso 5 (~8 min): Concurrencia y exclusión mutua con `threading.Lock`.

Corre `uv run onramp inspect --paso 5` para ver cómo 5 hilos sincronizados con `Barrier(5)`
reservan la misma sala al mismo tiempo. Protege la sección crítica con `threading.Lock`.
"""

import threading
import time


class RoomReservationService:
    """Gestiona reservas exclusivas de salas de estudio."""

    def __init__(self) -> None:
        # TODO 1: Crea `self._lock = threading.Lock()` y úsalo en `reserve` y `reservation_count`
        # para evitar que varios hilos reserven la misma sala al mismo tiempo.
        self._reservations: dict[str, list[str]] = {}
        _ = threading

    def reserve(self, room_code: str, user_id: str, delay_seconds: float = 0.01) -> bool:
        """Reserva una sala solo si sigue libre; devuelve True si ganó el cupo."""
        if self._reservations.get(room_code):
            return False
        if delay_seconds > 0:
            time.sleep(delay_seconds)
        self._reservations.setdefault(room_code, []).append(user_id)
        return True

    def reservation_count(self, room_code: str) -> int:
        """Devuelve cuántas reservas quedaron registradas para la sala."""
        return len(self._reservations.get(room_code, []))
