"""
Модуль для управления системой абонентов телефонной станции.
Включает описание услуг, данные абонентов и функции администратора.
"""
from dataclasses import dataclass


@dataclass
class Service:
    """Класс для представления услуги телефонной связи."""
    name: str
    price: float

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class Subscriber:
    """Класс для хранения данных об абоненте и его балансе."""
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.balance = 0
        self.services = []
        self.is_active = True

    def pay_bill(self, amount):
        """Абонент оплачивает счет"""
        self.balance += amount
        print(f"[Абонент]: Счет оплачен на {amount} руб. Баланс: {self.balance}")

    def __str__(self):
        status = "Подключен" if self.is_active else "ОТКЛЮЧЕН ЗА НЕУПЛАТУ"
        srv_names = [srv.name for srv in self.services]
        serv_list = ", ".join(srv_names) if self.services else "нет"

        return (f"\n Данные системы \n"
                f"Абонент: {self.name}\n"
                f"Номер: {self.phone_number}\n"
                f"Баланс: {self.balance} руб.\n"
                f"Статус: {status}\n"
                f"Услуги: {serv_list}\n")


class Administrator:
    """Класс для выполнения административных действий над абонентами."""
    def change_number(self, subscriber, new_number):
        """Администратор изменяет номер"""
        subscriber.phone_number = new_number
        print(f"[Админ]: Номер абонента {subscriber.name} изменен.")

    def add_service(self, subscriber, new_srv):
        """Администратор подключает услугу"""
        # Исправлено: аргумент переименован в new_srv
        subscriber.services.append(new_srv)
        print(f"[Админ]: Услуга '{new_srv.name}' добавлена.")

    def remove_service(self, subscriber, service_name):
        """Администратор отключает услугу по просьбе абонента"""
        for srv in subscriber.services:
            if srv.name.lower() == service_name.lower():
                subscriber.services.remove(srv)
                print(f"[Админ]: Услуга '{service_name}' удалена.")
                return
        print(f"[Админ]: Услуга '{service_name}' не найдена.")

    def manage_connection(self, subscriber):
        """Администратор временно отключает за неуплату"""
        if subscriber.balance < 0:
            subscriber.is_active = False
            print(f"[Админ]: Абонент {subscriber.name} ОТКЛЮЧЕН.")
        else:
            subscriber.is_active = True
            print(f"[Админ]: Абонент {subscriber.name} активен.")


all_services = [
    Service("Интернет", 400),
    Service("СМС-пакет", 100),
    Service("Межгород", 250)
]

print(" Вход в систему Телефонной Станции")
u_name = input("Введите имя нового абонента: ")
u_phone = input("Введите номер телефона: ")
sub = Subscriber(u_name, u_phone)
admin = Administrator()

while True:
    print("\nМЕНЮ:")
    print("1. Показать состояние")
    print("2. Оплатить счет")
    print("3. Списать за разговоры")
    print("4. Сменить номер")
    print("5. Подключить услугу")
    print("6. Отказаться от услуги")
    print("7. Проверить статус")
    print("0. Выход")

    choice = input("\nВыберите действие: ")

    if choice == "1":
        print(sub)
    elif choice == "2":
        money = float(input("Введите сумму оплаты: "))
        sub.pay_bill(money)
    elif choice == "3":
        debt = float(input("Введите стоимость разговоров: "))
        sub.balance -= debt
        print(f"Баланс: {sub.balance} руб.")
    elif choice == "4":
        new_num = input("Введите новый номер: ")
        admin.change_number(sub, new_num)
    elif choice == "5":
        print("\nСписок услуг:")
        # Исправлено: переменная цикла переименована в srv_item
        for i, srv_item in enumerate(all_services):
            print(f"{i+1}. {srv_item}")
        s_idx = int(input("Выберите номер услуги: ")) - 1
        admin.add_service(sub, all_services[s_idx])
    elif choice == "6":
        name_to_del = input("Введите название услуги: ")
        admin.remove_service(sub, name_to_del)
    elif choice == "7":
        admin.manage_connection(sub)
    elif choice == "0":
        break
    else:
        print("Неверный ввод.")
