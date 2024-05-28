import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cur = self.conn.cursor()

    def verification_of_authorization(self):
        self.name = input("Введите имя:")
        self.password = input("Введите пароль:")
        self.cur.execute("SELECT * FROM Users WHERE Login = ? AND Password = ?",(self.name, self.password, ))
        check = self.cur.fetchone()
        if check:
            print(f"Авторизация прошла успешно!\nЗдравствуйте {check[1]}")




if __name__=='__main__':
    a = DataBase()
    a.verification_of_authorization()