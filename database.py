import sqlite3
import os
from tkinter import Tk, filedialog
import pandas as pd

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS TypeOfUsers (
            Code        INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            Description TEXT    NOT NULL
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            ID         INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            Name       TEXT    NOT NULL,
            TypeOfUser TEXT    NOT NULL,
            Login      TEXT    NOT NULL
                               UNIQUE,
            Password   TEXT    NOT NULL,
            FOREIGN KEY (TypeOfUser)
            REFERENCES TypeOfUsers (Code) ON DELETE NO ACTION
                                          ON UPDATE CASCADE,
            UNIQUE (ID)
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Tests (
            Code             INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            Name             TEXT    NOT NULL,
            Creator          INTEGER NOT NULL,
            [Group]          INTEGER NOT NULL
                                     REFERENCES [Group] (Code) ON DELETE NO ACTION
                                                               ON UPDATE CASCADE,
            NumberOfAttempts INTEGER NOT NULL,
            FOREIGN KEY (Creator)
            REFERENCES Users (ID) 
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS TestResults (
            IDResult   INTEGER PRIMARY KEY ASC AUTOINCREMENT
                           NOT NULL,
            CodeTest   INTEGER REFERENCES Tests (Code) ON DELETE NO ACTION
                                                       ON UPDATE CASCADE,
            Evaluation INTEGER,
            IDStudent  INTEGER REFERENCES Users (ID) ON DELETE NO ACTION
                                                     ON UPDATE CASCADE
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS TeachersGroups (
            IDTeacher INTEGER REFERENCES Users (ID) ON DELETE NO ACTION
                                                    ON UPDATE CASCADE,
            CodeGroup INTEGER REFERENCES [Group] (Code) ON DELETE NO ACTION
                                                        ON UPDATE CASCADE
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Questions (
            Code        INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            Description TEXT    NOT NULL,
            CodeTest    INTEGER NOT NULL,
            FOREIGN KEY (CodeTest)
            REFERENCES Tests (Code) 
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS [Group] (
            Code      INTEGER PRIMARY KEY ASC AUTOINCREMENT
                              UNIQUE
                              NOT NULL,
            NameGroup TEXT    NOT NULL
                              UNIQUE
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS BandMembers (
            CodeGroup INTEGER REFERENCES [Group] (Code) ON DELETE NO ACTION
                                                        ON UPDATE CASCADE,
            IDStudent INTEGER REFERENCES Users (ID) ON DELETE NO ACTION
                                                    ON UPDATE CASCADE
        );
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Answers (
            Code          INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            Description   TEXT    NOT NULL,
            Accuracy      BOOLEAN NOT NULL,
            CodeQuestions INTEGER NOT NULL,
            FOREIGN KEY (CodeQuestions)
            REFERENCES Questions (Code) 
        );
        ''')

        # Вставка данных для тестирования
        # self.cur.execute("INSERT INTO TypeOfUsers (Description) VALUES ('Admin')")
        # self.cur.execute("INSERT INTO TypeOfUsers (Description) VALUES ('Tutore')")
        # self.cur.execute("INSERT INTO TypeOfUsers (Description) VALUES ('Teacher')")
        # self.cur.execute("INSERT INTO TypeOfUsers (Description) VALUES ('Student')")

        # self.cur.execute("INSERT INTO Users (Name, TypeOfUser, Login, Password) VALUES ('Admin User', '1', 'admin', 'adminpass')")
        # self.cur.execute("INSERT INTO Users (Name, TypeOfUser, Login, Password) VALUES ('Tutore User', '2', 'tutore', 'tutorepass')")
        # self.cur.execute("INSERT INTO Users (Name, TypeOfUser, Login, Password) VALUES ('Teacher User', '3', 'teacher', 'teacherpass')")
        # self.cur.execute("INSERT INTO Users (Name, TypeOfUser, Login, Password) VALUES ('Student User', '4', 'student', 'studentpass')")

        self.conn.commit()

    def verification_of_authorization(self):
        self.name = input("Введите имя: ")
        self.password = input("Введите пароль: ")
        self.cur.execute("SELECT * FROM Users WHERE Login = ? AND Password = ?", (self.name, self.password))
        user = self.cur.fetchone()
        if user:
            print(f"Авторизация прошла успешно!\nЗдравствуйте {user[1]}")
            return user
        else:
            raise Exception("Пользователь не найден")

    def add_user(self, name, login, password, role):
        self.cur.execute("INSERT INTO Users (Name, TypeOfUser, Login, Password) VALUES (?, ?, ?, ?)", (name, role, login, password))
        self.conn.commit()
        print(f"Пользователь {name} добавлен успешно")

    def delete_user(self, login):
        self.cur.execute("DELETE FROM Users WHERE Login = ?", (login,))
        self.conn.commit()
        print(f"Пользователь с логином {login} удален успешно")

    def edit_user(self, login, name, password, role):
        self.cur.execute("UPDATE Users SET Name = ?, Password = ?, TypeOfUser = ? WHERE Login = ?", (name, password, role, login))
        self.conn.commit()
        print(f"Пользователь с логином {login} обновлен успешно")

    def create_group(self, group_name):
        self.cur.execute("INSERT INTO [Group] (NameGroup) VALUES (?)", (group_name,))
        self.conn.commit()
        print(f"Группа {group_name} создана успешно")

    def add_student_to_group(self, group_name, student_login):
        self.cur.execute("SELECT Code FROM [Group] WHERE NameGroup = ?", (group_name,))
        group_code = self.cur.fetchone()
        self.cur.execute("SELECT ID FROM Users WHERE Login = ?", (student_login,))
        student_id = self.cur.fetchone()
        self.cur.execute("INSERT INTO BandMembers (CodeGroup, IDStudent) VALUES (?, ?)", (group_code[0], student_id[0]))
        self.conn.commit()
        print(f"Студент {student_login} добавлен в группу {group_name} успешно")

    def add_teacher_to_group(self, group_name, teacher_login):
        self.cur.execute("SELECT Code FROM [Group] WHERE NameGroup = ?", (group_name,))
        group_code = self.cur.fetchone()
        self.cur.execute("SELECT ID FROM Users WHERE Login = ?", (teacher_login,))
        teacher_id = self.cur.fetchone()
        self.cur.execute("INSERT INTO TeachersGroups (CodeGroup, IDTeacher) VALUES (?, ?)", (group_code[0], teacher_id[0]))
        self.conn.commit()
        print(f"Преподаватель {teacher_login} добавлен в группу {group_name} успешно")

    def import_users(self):
        # Создаем скрытое окно Tkinter
        window = Tk()
        window.withdraw()
        window.attributes("-topmost",True)

        # Открываем диалоговое окно для выбора файла
        file_path = filedialog.askopenfilename()

        # Проверяем, выбран ли файл
        if file_path:
            
            role = input("Выберите роль: 1-Админестратор, 2-Куратор, 3-Преподаватель, 4-Ученик")
            
            data = pd.read_csv(file_path)

            for user in data:
                user_data = user.split(';')

                print(user_data)
                # self.cur.execute("INSERT INTO Users (Name, TypeOfUser, Login, Password) VALUES (?, ?, ?, ?)", (user_data[0], role, user_data[1], user_data[2]))

            print(data[0])
        else:
            print("Файл не выбран")