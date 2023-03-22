import time

from app.client.user import User
from app.client.requests_to_server import Client


class Order:

    def __init__(self, start=None, finish=None, day=None, month=None, year=2023, hours=None, date=None, order_id=None):
        self.start = start
        self.finish = finish
        self.day = day
        self.month = month
        self.year = year
        self.hours = hours
        self.date = date
        self.order_id = order_id

    def __str__(self):
        return f'{self.__dict__}'

    def convert_time(self):
        try:
            self.day = str(self.day)
            self.month = str(self.month)
            self.day = int(self.day[1]) if self.day[0] == "0" else int(self.day)
            self.month = int(self.month[1]) if self.month[0] == "0" else int(self.month)
            self.year = int(self.year)

            if not (self.day in range(1, 32)):
                return "Недопустимый день"
            if not (self.month in range(1, 13)):
                return "Недопустимый месяц"
            if not (self.year in (2023, 2024)):
                return "Недопустимый год"

            date_list = self.year, self.month, self.day, int(self.hours[:-3]) + 3, 0, 0, 0, 0, 0
            self.date = int(time.mktime(date_list))
            return 'Accept'

        except ValueError:
            return 'Введите целые числа'

        except Exception as e:
            print(e, self)
            return 'Сервер недоступен'

    def find_companion(self, user: User):
        if not(self.start and self.finish and self.day and self.month and self.year and self.hours):
            return "Найти попутчика не удалось \n Заполнены не все данные"
        if self.start == self.finish:
            return "Некорректный маршрут"
        answer = self.convert_time()
        if answer != 'Accept':
            return answer

        order_data = {
            "status": 200,
            "process": "find_companion",
            "data": {
                "user_id": user.user_id,
                "start": self.start,
                "finish": self.finish,
                "date": self.date
            }
        }
        answer = Client().send_data_and_get_answer(order_data)

        if answer["status"] == 200:
            user.orders = answer.get("orders")
            return 'Accept'
        elif answer["status"] == "Failed":
            return "Не удалось установить \n соединение с сервером"
        else:
            return "Неизвестная ошибка"

    def find_order_by_id(self, user: User):
        order_data = {
            "status": 200,
            "process": "find_by_id",
            "data": self.order_id,
        }
        answer = Client().send_data_and_get_answer(order_data)

        if answer["status"] == 200:
            user.orders = answer.get("orders")
            return 'Accept'
        elif answer["status"] == "Failed":
            return "Не удалось установить \n соединение с сервером"
        else:
            return "Неизвестная ошибка"

    def delete_order_by_id(self, user: User):
        order_data = {
            "status": 200,
            "process": "delete",
            "data": self.order_id,
        }
        answer = Client().send_data_and_get_answer(order_data)

        if answer["status"] == 'Deleted':
            return "Deleted"
        elif answer["status"] == "Failed":
            return "Не удалось установить \n соединение с сервером"
        else:
            return "Неизвестная ошибка"


if __name__ == '__main__':
    pass
