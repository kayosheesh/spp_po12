"""Модуль реализует кофейный автомат (паттерн Factory Method)."""

from abc import ABC, abstractmethod


class Coffee(ABC):  # pylint: disable=too-few-public-methods
    """Абстрактный класс кофейного напитка."""

    @abstractmethod
    def prepare(self) -> str:
        """Приготовить напиток."""


class Espresso(Coffee):  # pylint: disable=too-few-public-methods
    """Класс напитка Espresso."""

    def prepare(self) -> str:
        """Приготовление эспрессо."""
        return "Готовится Espresso"


class Americano(Coffee):  # pylint: disable=too-few-public-methods
    """Класс напитка Americano."""

    def prepare(self) -> str:
        """Приготовление американо."""
        return "Готовится Americano"


class Latte(Coffee):  # pylint: disable=too-few-public-methods
    """Класс напитка Latte."""

    def prepare(self) -> str:
        """Приготовление латте."""
        return "Готовится Latte"


class Cappuccino(Coffee):  # pylint: disable=too-few-public-methods
    """Класс напитка Cappuccino."""

    def prepare(self) -> str:
        """Приготовление капучино."""
        return "Готовится Cappuccino"


class Mocha(Coffee):  # pylint: disable=too-few-public-methods
    """Класс напитка Mocha."""

    def prepare(self) -> str:
        """Приготовление мокка."""
        return "Готовится Mocha"


class CoffeeFactory:  # pylint: disable=too-few-public-methods
    """Фабрика кофейных напитков."""

    @staticmethod
    def create_coffee(coffee_type: str) -> Coffee:
        """Создать объект кофе."""
        coffees = {
            "espresso": Espresso,
            "americano": Americano,
            "latte": Latte,
            "cappuccino": Cappuccino,
            "mocha": Mocha,
        }

        coffee_class = coffees.get(coffee_type.lower())

        if coffee_class is None:
            raise ValueError("Неизвестный тип кофе")

        return coffee_class()


class CoffeeMachine:  # pylint: disable=too-few-public-methods
    """Класс кофейного автомата."""

    def order(self, coffee_type: str) -> str:
        """Заказать кофе."""
        coffee = CoffeeFactory.create_coffee(coffee_type)
        return coffee.prepare()


def main() -> None:
    """Точка входа."""
    machine = CoffeeMachine()
    coffee_type = input("Введите тип кофе: ")
    print(machine.order(coffee_type))


if __name__ == "__main__":
    main()
