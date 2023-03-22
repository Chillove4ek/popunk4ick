import time
import _sqlite3


class DatabaseManager:

    def __init__(self, base_name=None):
        self.conn = _sqlite3.connect(base_name)
        self.cursor = self.conn.cursor()

    def get_user(self, user):
        request = f"""
            SELECT Userid, password, link
            FROM Users
            Where Account = '{user.get("data")["username"]}'
        """
        self.cursor.execute(request)
        result_checking = self.cursor.fetchall()
        if not result_checking:
            return {"status": "NoUser", }

        db_user = result_checking[0]
        if db_user[1] != user.get("data")["password"]:
            return {"status": "Incorrect password", }

        answer = {
            "status": "Accepted",
            "user_id": db_user[0],
            "link": db_user[2],
        }
        return answer

    def add_user_to_db(self, data):
        request = f"""
            SELECT Userid, password
            FROM Users
            Where Account = '{data.get("data").get("username")}'
        """
        self.cursor.execute(request)
        result_checking = self.cursor.fetchall()
        if result_checking:
            return {"status": "Taken"}
        self.cursor.execute("""
            INSERT into Users(Account, password, link) Values(?,?, ?);
        """, list(data.get("data").values()))
        self.conn.commit()
        answer = {
            "status": "Accept",
            "user_id": self.get_user(data).get("user_id")
        }
        return answer

    def find_my_orders(self, data):
        request = f"""
             SELECT OrderID, StartPoint, FinishPoint, Date
             FROM Orders
             Where 
                 UserID = '{data["data"]}'
            ORDER BY Date
         """
        self.cursor.execute(request)
        result_checking = self.cursor.fetchall()
        return {
            "status": 200,
            "orders": result_checking
        }

    def refresh_link(self, user):
        request = f"""
            UPDATE Users
            SET link = '{user["data"]["link"]}'
            Where 
                UserID = '{user["data"]["user_id"]}'
                """
        self.cursor.execute(request)
        self.cursor.fetchall()
        self.conn.commit()
        return {"status": 200}

    def add_order_to_db(self, data):
        request = f"""
            SELECT *
            FROM Orders
            Where 
                Orders.UserID = '{data["data"]["user_id"]}' AND
                Orders.StartPoint = '{data["data"]["start"]}' AND
                Orders.FinishPoint = '{data["data"]["finish"]}' AND
                Orders.Date = '{data["data"]["start"]}'                
       """
        self.cursor.execute(request)
        result_checking = self.cursor.fetchall()
        if not result_checking:
            self.cursor.execute("""
                INSERT into ORDERS(UserID, startpoint, Finishpoint, Date) Values(?,?,?,?);
            """, list(data.get("data").values()))
            self.conn.commit()

    def find_friend(self, data):
        request = f"""
            SELECT Users.Account, Users.link, Orders.Date
            FROM Orders
            INNER JOIN Users
            ON Orders.UserID = Users.UserID
            Where 
                Orders.UserID != '{data["data"]["user_id"]}' AND
                Orders.StartPoint = '{data["data"]["start"]}' AND
                Orders.FinishPoint = '{data["data"]["finish"]}' AND
                Orders.Date > {time.time()}
            ORDER BY ABS(Date - {int(data["data"]["date"])})
            LIMIT 10
        """
        self.cursor.execute(request)
        result_checking = self.cursor.fetchall()
        answer = {
            "status": 200,
            "orders": result_checking,
        }
        return answer

    def find_by_orderid(self, data):
        request = f"""
            SELECT UserID, StartPoint, FinishPoint, Date
            FROM Orders
            Where 
                OrderID == '{data["data"]}' 
        """
        self.cursor.execute(request)
        result_checking = self.cursor.fetchall()
        order = result_checking[0]
        new_data = {
            "user_id": order[0],
            "start": order[1],
            "finish": order[2],
            "date": order[3],
        }
        return self.find_friend(data={"data": new_data})

    def delete_order(self, data):
        request = f"""
            DELETE
            FROM Orders
            Where 
                OrderID = '{data["data"]}'
                """
        self.cursor.execute(request)
        self.cursor.fetchall()
        self.conn.commit()
        answer = {"status": "Deleted"}
        return answer


if __name__ == '__main__':
    pass
