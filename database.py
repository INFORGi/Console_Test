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
        # Проверяем, существует ли пользователь с таким логином
        self.cur.execute("SELECT COUNT(*) FROM Users WHERE Login=?", (login,))
        count = self.cur.fetchone()
        if count != None:
            print(f"Ошибка: Пользователь с логином {login} уже существует")
        else:
            # Если пользователь с таким логином не существует, добавляем его
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
        # Проверяем, существует ли группа с таким названием
        self.cur.execute("SELECT Code FROM [Group] WHERE NameGroup = ?", (group_name,))
        count = self.cur.fetchone()
        
        if count != None:
            print(f"Ошибка: Группа с названием {group_name} уже существует")
        else:
            self.cur.execute("INSERT INTO [Group] (NameGroup) VALUES (?)", (group_name,))
            self.conn.commit()
            print(f"Группа {group_name} создана успешно")

    def add_student_to_group(self, group_name, student_login):
        # Проверяем, существует ли группа с таким названием
        self.cur.execute("SELECT Code FROM [Group] WHERE NameGroup = ?", (group_name,))
        group_code = self.cur.fetchone()

        # Проверяем, существует ли студент с указанным логином
        self.cur.execute("SELECT ID FROM Users WHERE Login = ?", (student_login,))
        student_id = self.cur.fetchone()

        if group_code is None:
            print(f"Ошибка: Группа с названием {group_name} не существует")
        elif student_id is None:
            print(f"Ошибка: Студент с логином {student_login} не существует")
        else:
            # Проверяем, есть ли студент уже в этой группе
            self.cur.execute("SELECT COUNT(*) FROM BandMembers WHERE CodeGroup = ? AND IDStudent = ?", (group_code[0], student_id[0]))
            count = self.cur.fetchone()[0]
            if count == 0:
                # Проверяем, состоит ли студент уже в какой-либо группе
                self.cur.execute("SELECT COUNT(*) FROM BandMembers WHERE IDStudent = ?", (student_id[0],))
                count = self.cur.fetchone()[0]
                if count == 0:
                    # Добавляем студента в группу
                    self.cur.execute("INSERT INTO BandMembers (CodeGroup, IDStudent) VALUES (?, ?)", (group_code[0], student_id[0]))
                    self.conn.commit()
                    print(f"Студент {student_login} добавлен в группу {group_name} успешно")
                else:
                    print(f"Ошибка: Студент {student_login} уже состоит в другой группе")
            else:
                print(f"Ошибка: Студент {student_login} уже состоит в группе {group_name}")


    def add_teacher_to_group(self, group_name, teacher_login):
        # Проверяем, существует ли группа с таким названием
        self.cur.execute("SELECT Code FROM [Group] WHERE NameGroup = ?", (group_name,))
        group_code = self.cur.fetchone()

        # Проверяем, существует ли преподаватель с указанным логином
        self.cur.execute("SELECT ID FROM Users WHERE Login = ?", (teacher_login,))
        teacher_id = self.cur.fetchone()

        if group_code is None:
            print(f"Ошибка: Группа с названием {group_name} не существует")
        elif teacher_id is None:
            print(f"Ошибка: Преподаватель с логином {teacher_login} не существует")
        else:
            # Проверяем, есть ли преподаватель уже в этой группе
            self.cur.execute("SELECT COUNT(*) FROM TeachersGroups WHERE CodeGroup = ? AND IDTeacher = ?", (group_code[0], teacher_id[0]))
            count = self.cur.fetchone()[0]
            if count == 0:
                # Добавляем преподавателя в группу
                self.cur.execute("INSERT INTO TeachersGroups (CodeGroup, IDTeacher) VALUES (?, ?)", (group_code[0], teacher_id[0]))
                self.conn.commit()
                print(f"Преподаватель {teacher_login} добавлен в группу {group_name} успешно")
            else:
                print(f"Ошибка: Преподаватель {teacher_login} уже состоит в группе {group_name}")



    def import_users(self):
        window = Tk()
        window.withdraw()
        window.attributes("-topmost", True)

        file_path = filedialog.askopenfilename()

        if file_path:
            role = input("Выберите роль: 1-Админестратор, 2-Куратор, 3-Преподаватель, 4-Ученик: ")
            data = pd.read_csv(file_path, header=None)  # Указываем, что у нас нет заголовка

            for index, row in data.iterrows():
                user_data = row[0].split(';')
                print(user_data)
                self.cur.execute("INSERT INTO Users (Name, TypeOfUser, Login, Password) VALUES (?, ?, ?, ?)",
                                 (user_data[0], role, user_data[1], user_data[2]))
                self.conn.commit()
            print("Пользователи успешно импортированны")
        else:
            print("Файл не выбран")