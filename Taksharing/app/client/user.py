from app.client.utilities import check_new_link
from app.client.requests_to_server import Client


class User:

    def __init__(self, username=None, password=None, password_check=None, link=None, user_id=None,
                 orders=None, last_screen=None):
        self.username = username
        self.password = password
        self.password_check = password_check
        self.link = link
        self.user_id = user_id
        self.orders = orders
        self.last_screen = last_screen

    def __str__(self):
        return f'{self.__dict__}'

    def get_link(self):
        return self.link or ''

    def login(self):
        if not(self.username and self.password):
            return 'Не заполнены данные'
        if "'" in self.username:
            return "Недопустимый символ ' в логине"

        user_data = {
            "status": 200,
            "process": "login",
            "data": {
                "username": self.username,
                "password": self.password
            }
        }
        answer = Client().send_data_and_get_answer(data=user_data)

        if answer["status"] == "Failed":
            return "Не удалось подключиться к серверу"
        elif answer["status"] == "Accepted":
            self.user_id = answer.get("user_id")
            self.link = answer.get("link")
            return "Accept"
        elif answer["status"] == "Incorrect password":
            return "Неверный пароль"
        elif answer["status"] == "NoUser":
            return "Пользователь не найден \n Зарегистрируйтесь"
        else:
            return "Неизвестная ошибка"

    def registration(self):
        if not(self.username and self.link and self.password and self.password_check):
            return "Зарегистрироваться не удалось \n Заполнены не все данные"
        if not check_new_link(self.link):
            return "Зарегистрироваться не удалось \n Неверная ссылка"
        if not (self.password == self.password_check):
            return "Пароли не совпадают"

        user_data = {
            "status": 200,
            "process": "register",
            "data": {
                "username": self.username,
                "password": self.password,
                "link": self.link
            }
        }
        answer = Client().send_data_and_get_answer(user_data)

        if answer["status"] == "Taken":
            return "Имя пользователя уже занято"
        elif answer["status"] == "Accept":
            self.user_id = answer["user_id"]
            return "Accept"
        elif answer["status"] == "Failed":
            return "Не удалось установить \n соединение с сервером"
        else:
            return "Неизвестная ошибка"

    def find_orders(self):
        user_data = {
            "status": 200,
            "process": "find_orders",
            "data": self.user_id
        }
        answer = Client().send_data_and_get_answer(user_data)

        if answer["status"] == 200:
            self.orders = answer["orders"]
            return "Completed"
        elif answer["status"] == "Failed":
            return "Не удалось установить \n соединение с сервером"
        else:
            return "Неизвестная ошибка"

    def update_link(self):
        if not check_new_link(self.link):
            return "Обновить ссылку невозможно \n Указана недопустимая ссылка"

        user_data = {
            "status": 200,
            "process": "refresh_link",
            "data": self.__dict__
        }
        answer = Client().send_data_and_get_answer(user_data)
        if answer["status"] == 200:
            return "Updated"
        elif answer["status"] == "Failed":
            return "Не удалось установить \n соединение с сервером"
        else:
            return "Неизвестная ошибка"


if __name__ == '__main__':
    pass
