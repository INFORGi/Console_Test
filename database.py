import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cur = self.conn.cursor()

    def verification_of_authorization(self):
        self.name = input("Введите имя:")
        self.password = input("Введите пароль:")
        self.cur.execute("SELECT * FROM Users WHERE Login = ? AND Password = ?",(self.name, self.password, ))
        user = self.cur.fetchone()
        if user:
            print(f"Авторизация прошла успешно!\nЗдравствуйте {user[1]}")
            return user
        else:
            return Exception("Пользоватеь не наеден")