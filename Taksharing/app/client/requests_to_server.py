import json
from socket import *

from settings.config import SERVER_IP, SERVER_PORT


class Client:
    def __init__(self, ip=SERVER_IP, port=SERVER_PORT, cli=None):
        self.ip = ip
        self.port = port
        self.cli = cli

    def ping_server(self):
        try:  # connecting to server
            self.cli = socket(AF_INET, SOCK_STREAM)
            self.cli.connect(
                (self.ip, self.port)
            )
        except ConnectionRefusedError as e:  # fail of connection
            print(e)

        try:  # getting success answer if connected and decoding it
            msg_pick = self.cli.recv(4096)
            msg = json.loads(msg_pick)
            if msg.get("connected_status") == 'Connected':
                return True
            else:
                return False
        except Exception as e:
            print(f"Error:{str(e)}")
            return False

    def send_data_and_get_answer(self, data):
        answer = {
            "status": 'Failed'
        }

        if self.ping_server():
            json_obj = json.dumps(data)
            self.cli.sendall(bytes(json_obj, encoding="utf-8"))
            try:
                answer_json = self.cli.recv(4096)
                if answer_json:
                    answer = json.loads(answer_json)
                    print(answer)
            finally:
                self.cli.close()
        return answer


if __name__ == '__main__':
    Client(ip='1.2.3.4')
