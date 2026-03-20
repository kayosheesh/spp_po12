"""
Модуль для работы с множеством вещественных чисел.
"""


class FloatSet:
    """Класс для представления множества вещественных чисел."""

    def __init__(self, *args):
        """Конструктор."""
        self._elements = []
        for num in args:
            self.add(num)

    @property
    def elements(self):
        """Геттер."""
        return self._elements.copy()

    def add(self, value):
        """Добавить элемент."""
        try:
            value = float(value)
            if value not in self._elements:
                self._elements.append(value)
                return True
            return False
        except (TypeError, ValueError):
            return False

    def remove(self, value):
        """Удалить элемент."""
        try:
            value = float(value)
            if value in self._elements:
                self._elements.remove(value)
                return True
            return False
        except (TypeError, ValueError):
            return False

    def contains(self, value):
        """Проверить принадлежность."""
        try:
            return float(value) in self._elements
        except (TypeError, ValueError):
            return False

    def union(self, other):
        """Объединение."""
        result = FloatSet()
        for elem in self._elements:
            result.add(elem)
        for elem in other.elements:
            result.add(elem)
        return result

    def __str__(self):
        """Строковое представление."""
        if not self._elements:
            return "{}"
        elems = ", ".join(str(e) for e in sorted(self._elements))
        return "{" + elems + "}"

    def __eq__(self, other):
        """Сравнение."""
        if not isinstance(other, FloatSet):
            return False
        return sorted(self._elements) == sorted(other._elements)

    def __contains__(self, value):
        """Оператор in."""
        return self.contains(value)

    def __len__(self):
        """Размер."""
        return len(self._elements)


def print_menu():
    """Меню."""
    print("\n" + "=" * 40)
    print("МЕНЮ")
    print("=" * 40)
    print("1. Показать")
    print("2. Добавить")
    print("3. Удалить")
    print("4. Проверить")
    print("5. Объединить")
    print("6. Сравнить")
    print("7. Новая")
    print("8. Выход")
    print("-" * 40)


def handle_show(s):
    """Показать."""
    print(f"\n{s}")
    print(f"Элементы: {', '.join(str(x) for x in sorted(s.elements))}")
    print(f"Количество: {len(s)}")
    return s


def handle_add(s):
    """Добавить."""
    try:
        val = float(input("Число: "))
        if s.add(val):
            print(f"{val} добавлено")
        else:
            print(f"{val} уже есть")
    except ValueError:
        print("Ошибка")
    return s


def handle_remove(s):
    """Удалить."""
    try:
        val = float(input("Число: "))
        if s.remove(val):
            print(f"{val} удалено")
        else:
            print(f"{val} не найдено")
    except ValueError:
        print("Ошибка")
    return s


def handle_contains(s):
    """Проверить."""
    try:
        val = float(input("Число: "))
        print(f"{val} {'есть' if val in s else 'нет'}")
    except ValueError:
        print("Ошибка")
    return s


def get_other_set():
    """Получить другое множество."""
    vals = input("Числа через пробел: ").split()
    other = FloatSet()
    for v in vals:
        try:
            other.add(float(v))
        except ValueError:
            continue
    return other


def handle_union(s):
    """Объединить."""
    other = get_other_set()
    if len(other) == 0:
        return s
    print(f"Первое: {s}")
    print(f"Второе: {other}")
    u = s.union(other)
    print(f"Результат: {u}")
    if input("Заменить? (д/н): ").lower() in ["д", "да"]:
        return u
    return s


def handle_compare(s):
    """Сравнить."""
    other = get_other_set()
    print(f"Текущее: {s}")
    print(f"Другое: {other}")
    print("Равны" if s == other else "Не равны")
    return s


def handle_new():
    """Создать новое."""
    return get_other_set()


def main():
    """Главная функция."""
    print("=" * 60)
    print("МНОЖЕСТВО ЧИСЕЛ")
    print("=" * 60)

    s = get_other_set()

    while True:
        print_menu()
        print(f"Текущее: {s}")
        choice = input("Выбор: ").strip()

        if choice == "1":
            s = handle_show(s)
        elif choice == "2":
            s = handle_add(s)
        elif choice == "3":
            s = handle_remove(s)
        elif choice == "4":
            s = handle_contains(s)
        elif choice == "5":
            s = handle_union(s)
        elif choice == "6":
            s = handle_compare(s)
        elif choice == "7":
            s = handle_new()
        elif choice == "8":
            print("Выход")
            break
        else:
            print("Неверный выбор")

        if choice != "8":
            input("\nEnter...")


if __name__ == "__main__":
    main()
