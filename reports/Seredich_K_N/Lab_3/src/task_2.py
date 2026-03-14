"""Модуль реализует адаптацию аналоговых часов к цифровым (Adapter)."""

from abc import ABC, abstractmethod


class DigitalClockInterface(ABC):  # pylint: disable=too-few-public-methods
    """Интерфейс цифровых часов."""

    @abstractmethod
    def get_time(self) -> str:
        """Получить время."""


class AnalogClock:  # pylint: disable=too-few-public-methods
    """Аналоговые часы."""

    def __init__(self, hour_angle: float, minute_angle: float) -> None:
        """Инициализация углов стрелок."""
        self.hour_angle = hour_angle
        self.minute_angle = minute_angle


class ClockAdapter(DigitalClockInterface):  # pylint: disable=too-few-public-methods
    """Адаптер аналоговых часов."""

    def __init__(self, analog_clock: AnalogClock) -> None:
        """Инициализация адаптера."""
        self.analog_clock = analog_clock

    def get_time(self) -> str:
        """Вернуть цифровое время."""
        hour = int(self.analog_clock.hour_angle / 30) % 12
        minute = int(self.analog_clock.minute_angle / 6)

        return f"{hour:02d}:{minute:02d}"


def main() -> None:
    """Точка входа."""
    hour_angle = float(input("Введите угол часовой стрелки: "))
    minute_angle = float(input("Введите угол минутной стрелки: "))

    analog = AnalogClock(hour_angle, minute_angle)
    adapter = ClockAdapter(analog)

    print("Цифровое время:", adapter.get_time())


if __name__ == "__main__":
    main()
