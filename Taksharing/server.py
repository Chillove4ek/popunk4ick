import json
import socket
import time
from socket import *

from server.database_manager import DatabaseManager


class Server:

    def __init__(self, ip: str, port: int, base_name=None, user=None, addr=None):
        print(f"Server IP:{ip}\nServer PORT:{port}\n")
        self.DB_manager = DatabaseManager(base_name=base_name)
        self.ser = socket(AF_INET, SOCK_STREAM)
        self.ser.bind((ip, port))
        self.ser.listen(5)
        self.user, self. addr = user, addr

    def start_server(self):
        while True:
            self.user, self.addr = self.ser.accept()
            print(f"Client CONNECTED:\n\tIP: {self.addr[0]}\n\tPORT: {self.addr[1]}\n"
                  f"{time.strftime('%d/%m/%Y, %H:%M', time.gmtime())}")
            self.listen()

    def listen(self):
        request = self.get_request()

        if request["status"] != 200:
            self.disconnect_user()
            return

        answer = self.get_answer(request)
        print(answer)
        self.send_answer_to_user(answer)

        self.disconnect_user()

    def get_request(self):
        connect_info = {
            "connected_status": "Connected",
        }
        json_obj = json.dumps(connect_info)
        self.user.sendall(bytes(json_obj, encoding="utf-8"))

        try:
            json_request = self.user.recv(4096)
            request = json.loads(json_request)
        except Exception as e:
            request = {
                "status": "500",
            }
            print(e)
        print(request)
        return request


    def get_answer(self, request):
        if request["process"] == "login":
            print("Вход...")
            answer = self.DB_manager.get_user(request)

        elif request["process"] == "register":
            print("Регистрирую нового пользователя")
            answer = self.DB_manager.add_user_to_db(request)

        elif request["process"] == "find_orders":
            print("Ищу заявки клиента")
            answer = self.DB_manager.find_my_orders(request)

        elif request['process'] == "refresh_link":
            print("Обновляю ссылку")
            answer = self.DB_manager.refresh_link(request)

        elif request["process"] == "find_companion":
            print("Ищу попутчиков..")
            self.DB_manager.add_order_to_db(request)
            answer = self.DB_manager.find_friend(request)

        elif request["process"] == "delete":
            print("Удаляю запись")
            answer = self.DB_manager.delete_order(request)

        elif request["process"] == "find_by_id":
            print("Ищу по номеру заявки")
            answer = self.DB_manager.find_by_orderid(request)

        else:
            print("Unknown movie!")
            answer = ("wtf",)
        return answer

    def disconnect_user(self):
        try:
            self.user.shutdown(SHUT_WR)
            print(self.user, "отключен")
        except Exception as e:
            print(f"Не удалось отключить пользователя {e}")
        return

    def send_answer_to_user(self, answer):
        try:
            json_obj = json.dumps(answer)
            self.user.sendall(bytes(json_obj, encoding="utf-8"))
            print("Отправил ответ!")
        except Exception as e:
            print(f"Произошла ошибка при отправке {e}")


if __name__ == '__main__':
    db_path = r"C:\Users\momyo\PycharmProjects\Taksharing\TaxiData.sqlite"
    Server(ip="127.0.0.1", port=8000, base_name=db_path).start_server()
