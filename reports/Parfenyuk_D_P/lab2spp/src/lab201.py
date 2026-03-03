"""
Модуль для работы с пользовательским классом CharacterSet.
Позволяет создавать ограниченные множества символов и выполнять операции над ними.
"""

class CharacterSet:
    """
    Класс для представления множества символов с фиксированной максимальной емкостью.
    """
    def __init__(self, capacity, initial_data=None):
        self.capacity = int(capacity)
        self.items = []
        if initial_data:
            for item in initial_data:
                self.add(item)

    def add(self, char):
        """Добавление элемента в множество"""
        if char not in self.items and len(self.items) < self.capacity:
            self.items.append(char)
            print(f"Успех: Символ '{char}' добавлен.")
        elif len(self.items) >= self.capacity:
            print(f"Ошибка: Лимит ({self.capacity}) исчерпан!")
        else:
            print(f"Инфо: Символ '{char}' уже есть в множестве.")

    def remove(self, char):
        """Удаление элемента из множества"""
        if char in self.items:
            self.items.remove(char)
            print(f"Успех: Символ '{char}' удален.")
        else:
            print(f"Ошибка: Символа '{char}' нет в этом множестве.")

    def belongs(self, char):
        """Принадлежит ли значение множеству (True/False)"""
        return char in self.items

    def union(self, other):
        """Объединение двух множеств"""
        new_set = CharacterSet(self.capacity + other.capacity)
        for item in self.items:
            new_set.add(item)
        for item in other.items:
            new_set.add(item)
        return new_set

    def __str__(self):
        """Вывод элементов на консоль"""
        if not self.items:
            return "{пусто}"
        return "{" + ", ".join(self.items) + "}"

    def __eq__(self, other):
        """Сравнение объектов типа CharacterSet"""
        if not isinstance(other, CharacterSet):
            return False
        return sorted(self.items) == sorted(other.items)


print("Начальный ввод ")
cap1 = input("Введите лимит для множества 1: ")
set1 = CharacterSet(cap1)

cap2 = input("Введите лимит для множества 2: ")
set2 = CharacterSet(cap2)

while True:
    print("\n" + "=" * 30)
    print(f"множество 1: {set1}")
    print(f"множество 2: {set2}")
    print("-" * 30)
    print("1. Добавить символ в множество 1")
    print("2. Добавить символ в множество 2")
    print("3. Удалить символ из множества 1")
    print("4. Проверить принадлежность (множество 1)")
    print("5. Объединить множества (1 + 2)")
    print("6. Сравнить множества (1 == 2)")
    print("0. Выход")

    choice = input("\nВыберите действие: ")

    if choice == "1":
        user_input = input("Введите символ: ")
        set1.add(user_input)

    elif choice == "2":
        user_input = input("Введите символ: ")
        set2.add(user_input)

    elif choice == "3":
        user_input = input("Какой символ удалить из Множества 1?: ")
        set1.remove(user_input)

    elif choice == "4":
        user_input = input("Какой символ ищем в Множестве 1?: ")
        if set1.belongs(user_input):
            print(f"Результат: Символ '{user_input}' входит в Множество 1.")
        else:
            print("Результат: Символа нет.")

    elif choice == "5":
        result_set = set1.union(set2)
        print(f"Результат объединения: {result_set}")
        print("(Новое множество создано на основе суммы лимитов)")

    elif choice == "6":
        if set1 == set2:
            print("Результат: Множества равны!")
        else:
            print("Результат: Множества разные.")

    elif choice == "0":
        print("Завершение работы.")
        break
    else:
        print("Неверный ввод, попробуйте еще раз.")
