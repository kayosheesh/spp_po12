"""Модуль реализует настраиваемый калькулятор (Command)."""

from abc import ABC, abstractmethod


class Command(ABC):  # pylint: disable=too-few-public-methods
    """Интерфейс команды."""

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Выполнить команду."""


class AddCommand(Command):  # pylint: disable=too-few-public-methods
    """Команда сложения."""

    def execute(self, a: float, b: float) -> float:
        """Сложение."""
        return a + b


class SubtractCommand(Command):  # pylint: disable=too-few-public-methods
    """Команда вычитания."""

    def execute(self, a: float, b: float) -> float:
        """Вычитание."""
        return a - b


class MultiplyCommand(Command):  # pylint: disable=too-few-public-methods
    """Команда умножения."""

    def execute(self, a: float, b: float) -> float:
        """Умножение."""
        return a * b


class Button:  # pylint: disable=too-few-public-methods
    """Кнопка калькулятора."""

    def __init__(self, command: Command) -> None:
        """Инициализация кнопки."""
        self.command = command

    def press(self, a: float, b: float) -> float:
        """Нажать кнопку."""
        return self.command.execute(a, b)

    def set_command(self, command: Command) -> None:
        """Изменить команду."""
        self.command = command


class Calculator:  # pylint: disable=too-few-public-methods
    """Калькулятор."""

    def __init__(self) -> None:
        """Инициализация."""
        self.add_button = Button(AddCommand())
        self.sub_button = Button(SubtractCommand())
        self.custom_button = Button(MultiplyCommand())


def main() -> None:
    """Точка входа."""
    calc = Calculator()

    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))

    print("Сложение:", calc.add_button.press(a, b))
    print("Вычитание:", calc.sub_button.press(a, b))
    print("Умножение:", calc.custom_button.press(a, b))


if __name__ == "__main__":
    main()
