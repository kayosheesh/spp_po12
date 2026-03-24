"""
Модуль моделирует работу транспортного маршрута.

Содержит абстрактный класс транспорта, его реализации
и класс маршрута с обработкой поломки транспорта.
"""

from abc import ABC, abstractmethod
from typing import Optional


class Transport(ABC):
    """
    Абстрактный базовый класс транспорта.
    """

    def __init__(self, number: str) -> None:
        """
        Инициализирует транспорт.

        :param number: Номер транспорта
        """
        self._number = number
        self._is_working = True

    @property
    def number(self) -> str:
        """
        Возвращает номер транспорта.
        """
        return self._number

    @property
    def is_working(self) -> bool:
        """
        Возвращает состояние транспорта.
        """
        return self._is_working

    def break_down(self) -> None:
        """
        Переводит транспорт в состояние неисправности.
        """
        self._is_working = False

    @abstractmethod
    def transport_type(self) -> str:
        """
        Возвращает тип транспорта.
        """


class Bus(Transport):
    """
    Класс автобуса.
    """

    def transport_type(self) -> str:
        """
        Возвращает тип транспорта.
        """
        return "Автобус"


class Trolleybus(Transport):
    """
    Класс троллейбуса.
    """

    def transport_type(self) -> str:
        """
        Возвращает тип транспорта.
        """
        return "Троллейбус"


class Route:
    """
    Класс маршрута общественного транспорта.
    """

    def __init__(self, name: str, interval: int) -> None:
        """
        Инициализирует маршрут.

        :param name: Название маршрута
        :param interval: Интервал движения в минутах
        """
        self._name = name
        self._interval = interval
        self._transport: Optional[Transport] = None
        self._reserve: Optional[Transport] = None

    def assign_transport(self, transport: Transport) -> None:
        """
        Назначает основной транспорт на маршрут.
        """
        self._transport = transport

    def assign_reserve(self, transport: Transport) -> None:
        """
        Назначает резервный транспорт.
        """
        self._reserve = transport

    def handle_breakdown(self) -> None:
        """
        Обрабатывает поломку транспорта.
        """
        if self._transport and not self._transport.is_working:
            if self._reserve:
                self._transport = self._reserve
                self._reserve = None
                print("На маршрут вышел резервный транспорт.")
            else:
                self._interval += 5
                print("Интервал движения увеличен.")

    def info(self) -> str:
        """
        Возвращает информацию о маршруте.
        """
        if self._transport:
            transport_info = (
                f"{self._transport.transport_type()} " f"№{self._transport.number}"
            )
        else:
            transport_info = "Транспорт не назначен"

        return (
            f"Маршрут {self._name}, "
            f"интервал {self._interval} мин., "
            f"{transport_info}"
        )


if __name__ == "__main__":
    route = Route("A1", 10)

    bus = Bus("101")
    reserve_bus = Bus("102")

    route.assign_transport(bus)
    route.assign_reserve(reserve_bus)

    print(route.info())

    bus.break_down()
    route.handle_breakdown()

    print(route.info())
