"""
Система Железнодорожная касса.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class Payable(ABC):
    """Интерфейс для оплаты."""

    @abstractmethod
    def execute_payment(self) -> bool:
        """Выполнить оплату."""

    @abstractmethod
    def get_payment_status(self) -> bool:
        """Получить статус оплаты."""

    @abstractmethod
    def get_payment_amount(self) -> float:
        """Получить сумму оплаты."""


class PaymentSystem(Payable):
    """Платежная система."""

    def __init__(self, amount_value: float):
        self.amount_value = amount_value
        self.payment_status = False

    def execute_payment(self) -> bool:
        """Выполнить оплату."""
        print(f"  Оплата {self.amount_value} руб...")
        self.payment_status = True
        return True

    def get_payment_status(self) -> bool:
        """Получить статус оплаты."""
        return self.payment_status

    def get_payment_amount(self) -> float:
        """Получить сумму оплаты."""
        return self.amount_value


class User:
    """Базовый класс пользователя."""

    def __init__(self, user_identifier: int, user_fullname: str):
        self.identifier = user_identifier
        self.fullname = user_fullname

    def get_fullname(self) -> str:
        """Получить имя."""
        return self.fullname

    def get_identifier(self) -> int:
        """Получить ID."""
        return self.identifier


class Passenger(User):
    """Пассажир."""

    def __init__(self, user_identifier: int, user_fullname: str, passport_data: str):
        super().__init__(user_identifier, user_fullname)
        self.passport_data = passport_data
        self.purchased_tickets = []

    def create_request(self, destination: str, date: str, time: str):
        """Создать заявку."""
        return Request(self, destination, date, time)

    def add_ticket(self, ticket):
        """Добавить билет."""
        self.purchased_tickets.append(ticket)

    def show_tickets(self):
        """Показать билеты."""
        if not self.purchased_tickets:
            print("  Нет билетов")
            return
        print("\nБилеты:")
        for t in self.purchased_tickets:
            print(f"  {t}")

    def get_tickets_count(self) -> int:
        """Количество билетов."""
        return len(self.purchased_tickets)

    def get_passport(self) -> str:
        """Паспорт."""
        return self.passport_data


class Administrator(User):
    """Администратор."""

    def __init__(self, user_identifier: int, user_fullname: str, job_position: str):
        super().__init__(user_identifier, user_fullname)
        self.job_position = job_position

    def get_position(self) -> str:
        """Должность."""
        return self.job_position

    def change_position(self, new_position: str):
        """Изменить должность."""
        self.job_position = new_position


class Train:
    """Поезд."""

    def __init__(self, train_number: str, route: List[str], prices: Dict[str, float]):
        self.train_number = train_number
        self.route = route
        self.prices = prices
        self.reserved = {}

    def get_price(self, destination: str):
        """Цена до станции."""
        return self.prices.get(destination)

    def is_available(self, date: str):
        """Проверить наличие мест."""
        return date not in self.reserved

    def reserve(self, date: str):
        """Забронировать место."""
        self.reserved[date] = True

    def get_number(self) -> str:
        """Номер поезда."""
        return self.train_number

    def get_route(self) -> List[str]:
        """Маршрут."""
        return self.route.copy()

    def get_destinations(self) -> List[str]:
        """Список назначений."""
        return list(self.prices.keys())

    def __str__(self):
        return f"Поезд {self.train_number}: {' -> '.join(self.route)}"


class Request:
    """Заявка."""

    def __init__(self, passenger: Passenger, dest: str, date: str, time: str):
        self.passenger = passenger
        self.destination = dest
        self.date = date
        self.time = time
        self.found = []

    def search(self, office):
        """Поиск поездов."""
        print(f"\nПоиск до {self.destination}...")
        for train in office.get_all_trains():
            if train.get_price(self.destination) and train.is_available(self.date):
                self.found.append(train)
        return self.found.copy()

    def get_found(self):
        """Получить найденные."""
        return self.found.copy()

    def get_destination(self):
        """Станция."""
        return self.destination

    def get_passenger(self):
        """Пассажир."""
        return self.passenger

    def get_date(self):
        """Дата."""
        return self.date

    def get_time(self):
        """Время."""
        return self.time

    def has_results(self) -> bool:
        """Есть результаты."""
        return len(self.found) > 0


class Ticket:
    """Билет."""

    _counter = 1000

    def __init__(self, ticket_data: dict):
        """Создание билета из словаря."""
        self.owner = ticket_data["owner"]
        self.train = ticket_data["train"]
        self.dest = ticket_data["dest"]
        self.date = ticket_data["date"]
        self.price = ticket_data["price"]
        Ticket._counter += 1
        self.code = f"T{Ticket._counter}"

    def get_code(self) -> str:
        """Код билета."""
        return self.code

    def get_owner(self) -> str:
        """Владелец."""
        return self.owner

    def get_price(self) -> float:
        """Цена."""
        return self.price

    def __str__(self):
        return f"Билет {self.code}: {self.owner} -> {self.dest}, " f"{self.date}, {self.price} руб."


class Invoice:
    """Счет."""

    _counter = 1000

    def __init__(self, customer: str, dest: str, train: str, amount: float):
        self.customer = customer
        self.dest = dest
        self.train = train
        self.amount = amount
        Invoice._counter += 1
        self.code = f"I{Invoice._counter}"
        self.payment = None

    def create_payment(self):
        """Создать платеж."""
        self.payment = PaymentSystem(self.amount)
        return self.payment

    def get_amount(self):
        """Сумма."""
        return self.amount

    def get_customer(self):
        """Клиент."""
        return self.customer

    def get_train(self):
        """Поезд."""
        return self.train

    def get_dest(self):
        """Назначение."""
        return self.dest

    def get_code(self):
        """Номер счета."""
        return self.code

    def is_paid(self) -> bool:
        """Оплачен ли счет."""
        return self.payment is not None and self.payment.get_payment_status()


class TicketOffice:
    """Касса."""

    def __init__(self, name: str):
        self.name = name
        self.trains = []
        self.requests = []
        self.sold = []
        self.invoices = []

    def add_train(self, train):
        """Добавить поезд."""
        self.trains.append(train)

    def add_request(self, request):
        """Добавить заявку."""
        self.requests.append(request)

    def get_all_trains(self):
        """Все поезда."""
        return self.trains.copy()

    def show_trains(self):
        """Показать поезда."""
        print(f"\nПоезда '{self.name}':")
        if not self.trains:
            print("  Нет")
            return
        for i, t in enumerate(self.trains, 1):
            print(f"  {i}. {t}")

    def create_invoice(self, request, idx):
        """Создать счет."""
        found = request.get_found()
        if not found or idx < 1 or idx > len(found):
            return None
        train = found[idx - 1]
        price = train.get_price(request.get_destination())
        if price is None:
            return None
        inv = Invoice(request.get_passenger().get_fullname(), request.get_destination(), train.get_number(), price)
        self.invoices.append(inv)
        return inv

    def process_payment(self, invoice):
        """Обработать оплату."""
        if invoice.is_paid():
            return None
        payment = invoice.create_payment()
        if payment.execute_payment():
            ticket_data = {
                "owner": invoice.get_customer(),
                "train": invoice.get_train(),
                "dest": invoice.get_dest(),
                "date": invoice.get_dest(),
                "price": invoice.get_amount(),
            }
            ticket = Ticket(ticket_data)
            self.sold.append(ticket)
            return ticket
        return None

    def get_trains_count(self) -> int:
        """Количество поездов."""
        return len(self.trains)

    def get_sold_count(self) -> int:
        """Количество проданных билетов."""
        return len(self.sold)

    def get_requests_count(self) -> int:
        """Количество заявок."""
        return len(self.requests)


def input_trains_data(office):
    """Ввод данных о поездах."""
    print("\nПОЕЗДА")
    cnt = int(input("Количество: "))

    for i in range(cnt):
        print(f"\n--- {i+1} ---")
        num = input("Номер: ")
        route = input("Маршрут (через пробел): ").split()
        prices = {}
        for s in route[1:]:
            prices[s] = float(input(f"Цена до {s}: "))
        office.add_train(Train(num, route, prices))


def handle_passenger_actions(office, passenger):
    """Обработка действий пассажира."""
    office.show_trains()

    print("\nЗАЯВКА")
    req = passenger.create_request(input("Куда: "), input("Дата (ГГГГ-ММ-ДД): "), input("Время: "))

    found = req.search(office)
    if not found:
        print("Ничего нет")
        return None

    print(f"\nНайдено: {len(found)}")
    for i, t in enumerate(found, 1):
        print(f"  {i}. {t.get_number()} - {t.get_price(req.get_destination())} руб.")

    choice = int(input(f"\nВыбрать (1-{len(found)}): "))
    inv = office.create_invoice(req, choice)
    if not inv:
        print("Ошибка")
        return None

    print(f"Сумма: {inv.get_amount()} руб.")
    return inv


def process_payment_flow(office, invoice, passenger):
    """Обработка оплаты."""
    if input("Платить? (д/н): ").lower() in ["д", "да"]:
        ticket = office.process_payment(invoice)
        if ticket:
            print("\nГОТОВО")
            print(ticket)
            passenger.add_ticket(ticket)
            return ticket
    return None


def show_final_stats(office, passenger):
    """Показать итоговую статистику."""
    trains_count = office.get_trains_count()
    sold_count = office.get_sold_count()

    print("\n" + "=" * 60)
    print(f"Поездов: {trains_count}")
    print(f"Продано: {sold_count}")
    passenger.show_tickets()
    print("=" * 60)


def main():
    """Главная функция."""
    print("=" * 60)
    print("ЖЕЛЕЗНОДОРОЖНАЯ КАССА")
    print("=" * 60)

    name = input("\nНазвание кассы: ")
    office = TicketOffice(name)

    print("\nАДМИНИСТРАТОР")
    admin_name = input("Имя: ")
    admin_pos = input("Должность: ")
    admin = Administrator(1, admin_name, admin_pos)
    print(f"Администратор {admin.get_fullname()} добавлен")

    input_trains_data(office)

    print("\nПАССАЖИР")
    p = Passenger(2, input("Имя: "), input("Паспорт: "))

    invoice = handle_passenger_actions(office, p)
    if invoice:
        process_payment_flow(office, invoice, p)

    show_final_stats(office, p)


if __name__ == "__main__":
    main()
