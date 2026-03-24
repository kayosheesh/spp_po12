"""Rectangle model with validation and utility methods."""


class Rectangle:
    """Represent a rectangle and provide basic geometry operations."""

    def __init__(self, a: float, b: float):
        """Initialize rectangle sides through validated properties."""
        self.a = a
        self.b = b

    @property
    def a(self):
        """Get side A value."""
        return self._a

    @a.setter
    def a(self, value):
        """Set side A ensuring it is a positive number."""
        if value <= 0:
            raise ValueError("Сторона должна быть положительным числом")
        self._a = value

    @property
    def b(self):
        """Get side B value."""
        return self._b

    @b.setter
    def b(self, value):
        """Set side B ensuring it is a positive number."""
        if value <= 0:
            raise ValueError("Сторона должна быть положительным числом")
        self._b = value

    def area(self) -> float:
        """Return rectangle area."""
        return self.a * self.b

    def perimeter(self) -> float:
        """Return rectangle perimeter."""
        return 2 * (self.a + self.b)

    def is_square(self) -> bool:
        """Check whether rectangle is a square."""
        return self.a == self.b

    def exists(self) -> bool:
        """Check whether rectangle sides are valid for existence."""
        return self.a > 0 and self.b > 0

    def __str__(self):
        """Return readable rectangle description."""
        return f"Прямоугольник со сторонами {self.a} и {self.b}"

    def __eq__(self, other):
        """Compare rectangles regardless of side order."""
        if not isinstance(other, Rectangle):
            return False
        return (self.a == other.a and self.b == other.b) or (
            self.a == other.b and self.b == other.a
        )


if __name__ == "__main__":
    r1 = Rectangle(5, 10)
    r2 = Rectangle(10, 5)

    print(r1)
    print("Площадь:", r1.area())
    print("Периметр:", r1.perimeter())
    print("Является квадратом:", r1.is_square())
    print("Существует:", r1.exists())
    print("Равны ли r1 и r2:", r1 == r2)
