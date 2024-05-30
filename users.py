class Admin:
    def __init__(self, db):
        self.db = db
    
    def add_user(self):
        print("Добавление нового пользователя")
        name = input("Имя: ")
        login = input("Логин: ")
        password = input("Пароль: ")
        role = input("Тип пользователя (1-Admin, 2-Tutore, 3-Teacher, 4-Student): ")
        self.db.add_user(name, login, password, role)
    
    def import_users(self):
        print("Импорт новых пользователей")
        self.db.import_users()

    def add_test(self):
        print("Добавление теста")
        # Реализация добавления теста

    def import_tests(self):
        print("Импорт тестов")
        # Реализация импорта тестов

    def delete_user(self):
        print("Удаление пользователя")
        login = input("Логин пользователя для удаления: ")
        self.db.delete_user(login)

    def edit_user(self):
        print("Редактирование пользователя")
        login = input("Логин пользователя для редактирования: ")
        name = input("Новое имя: ")
        password = input("Новый пароль: ")
        role = input("Новый тип пользователя (1-Admin, 2-Tutore, 3-Teacher, 4-Student): ")
        self.db.edit_user(login, name, password, role)

    def create_group(self):
        print("Создание группы")
        group_name = input("Название группы: ")
        self.db.create_group(group_name)

    def fill_group(self):
        print("Заполнение группы")
        group_name = input("Название группы: ")
        student_login = input("Логин студента: ")
        self.db.add_student_to_group(group_name, student_login)

class Tutore(Admin):
    def add_teacher_to_group(self):
        print("Добавление преподавателя в группу")
        group_name = input("Название группы: ")
        teacher_login = input("Логин преподавателя: ")
        self.db.add_teacher_to_group(group_name, teacher_login)
    
    def manage_tests(self):
        print("Добавление/редактирование тестов")
        # Реализация добавления/редактирования тестов

class Teacher:
    def __init__(self, db):
        self.db = db

    def add_test(self):
        print("Добавление тестов")
        # Реализация добавления тестов

    def view_test_results(self):
        print("Просмотр результатов тестов")
        # Реализация просмотра результатов тестов

class Student:
    def __init__(self, db):
        self.db = db

    def take_test(self):
        print("Прохождение тестов")
        # Реализация прохождения тестов