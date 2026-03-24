"""
Модуль, реализующий класс равнобедренного треугольника.

Содержит методы для проверки существования треугольника,
вычисления периметра, площади и сравнения объектов.
"""

from math import sqrt


class IsoscelesTriangle:
    """
    Класс, представляющий равнобедренный треугольник.

    Атрибуты:
        side_a (float): Боковая сторона.
        side_b (float): Боковая сторона (должна быть равна side_a).
        base (float): Основание треугольника.
    """

    def __init__(self, side_a: float, side_b: float, base: float) -> None:
        """
        Инициализирует равнобедренный треугольник.

        :param side_a: Первая боковая сторона
        :param side_b: Вторая боковая сторона
        :param base: Основание
        """
        self._side_a = side_a
        self._side_b = side_b
        self._base = base

    @property
    def side_a(self) -> float:
        """
        Возвращает первую боковую сторону.
        """
        return self._side_a

    @property
    def side_b(self) -> float:
        """
        Возвращает вторую боковую сторону.
        """
        return self._side_b

    @property
    def base(self) -> float:
        """
        Возвращает основание треугольника.
        """
        return self._base

    def exists(self) -> bool:
        """
        Проверяет существование равнобедренного треугольника.

        :return: True, если треугольник существует, иначе False
        """
        if self._side_a <= 0 or self._side_b <= 0 or self._base <= 0:
            return False
        if self._side_a != self._side_b:
            return False
        return self._side_a + self._side_b > self._base

    def perimeter(self) -> float:
        """
        Вычисляет периметр треугольника.

        :return: Периметр или 0.0, если треугольник не существует
        """
        if not self.exists():
            return 0.0
        return self._side_a + self._side_b + self._base

    def area(self) -> float:
        """
        Вычисляет площадь треугольника.

        :return: Площадь или 0.0, если треугольник не существует
        """
        if not self.exists():
            return 0.0
        height = sqrt(self._side_a**2 - (self._base / 2) ** 2)
        return (self._base * height) / 2

    def __str__(self) -> str:
        """
        Возвращает строковое представление треугольника.
        """
        return (
            "Равнобедренный треугольник: "
            f"боковые стороны = {self._side_a}, "
            f"основание = {self._base}"
        )

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает два треугольника на равенство.

        :param other: Другой объект
        :return: True, если треугольники равны
        """
        if not isinstance(other, IsoscelesTriangle):
            return False
        return (
            self._side_a == other.side_a
            and self._side_b == other.side_b
            and self._base == other.base
        )


if __name__ == "__main__":
    triangle1 = IsoscelesTriangle(5, 5, 6)
    triangle2 = IsoscelesTriangle(5, 5, 6)

    print(triangle1)
    print("Существует ли:", triangle1.exists())
    print("Периметр:", triangle1.perimeter())
    print("Площадь:", triangle1.area())
    print("Треугольники равны:", triangle1 == triangle2)
