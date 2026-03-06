class LimitedSet:
    def __init__(self, capacity, items=None):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self._capacity = capacity
        self._items = []

        if items is not None:
            for x in items:
                if isinstance(x, int) and x not in self._items:
                    if len(self._items) >= capacity:
                        raise ValueError("Items count exceeds capacity")
                    self._items.append(x)

    @property
    def cap(self):
        return self._capacity

    @property
    def size(self):
        return len(self._items)

    def add(self, x):
        if not isinstance(x, int):
            raise TypeError("Need integer")

        if x in self._items:
            return False

        if len(self._items) >= self._capacity:
            raise OverflowError("Set is full")

        self._items.append(x)
        return True

    def remove(self, x):
        if isinstance(x, int) and x in self._items:
            self._items.remove(x)
            return True
        return False

    def contains(self, x):
        return isinstance(x, int) and x in self._items

    def __iter__(self):
        return iter(self._items.copy())

    def __len__(self):
        return len(self._items)

    def __contains__(self, x):
        return self.contains(x)

    def union(self, other):
        if not isinstance(other, LimitedSet):
            raise TypeError("Expected LimitedSet")

        combined_set = set(self) | set(other)
        total_capacity = self.cap + other.cap

        if len(combined_set) > total_capacity:
            raise ValueError("Not enough capacity for union")

        return LimitedSet(total_capacity, combined_set)

    def display(self):
        elements = ", ".join(map(str, self._items)) if self._items else "пусто"
        print(f"Elements: {elements} [{self.size}/{self.cap}]")

    def __str__(self):
        if self._items:
            elements = ", ".join(map(str, self._items))
            return f"LimitedSet({{{elements}}}, {self.size}/{self.cap})"
        return f"LimitedSet(empty, {self.cap})"

    def __eq__(self, other):
        if not isinstance(other, LimitedSet):
            return False
        return set(self) == set(other)

    def __or__(self, other):
        return self.union(other)


if __name__ == "__main__":
    s1 = LimitedSet(5, [1, 2, 3])
    s2 = LimitedSet(3)
    s2.add(10)
    s2.add(20)

    print(s1)
    print(s2)

    print(f"Contains 2? {s1.contains(2)}")
    print(f"Contains 2? {2 in s1}")

    s1.remove(2)
    print(s1)

    s3 = s1.union(s2)
    print(f"Union: {s3}")

    s4 = s1 | s2
    print(f"Union with |: {s4}")

    print(f"Equals? {s1 == LimitedSet(5, [1, 3])}")

    print("Elements in s1:")
    for item in s1:
        print(f"  {item}")
