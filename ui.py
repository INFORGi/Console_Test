import users

class UI:
    def __init__(self, db):
        try:
            self.db = db
            user = self.db.verification_of_authorization()
            
            user_type = user[2]
            if user_type == '1':
                self.admin_menu(users.Admin(self.db))
            elif user_type == '2':
                self.tutore_menu(users.Tutore(self.db))
            elif user_type == '3':
                self.teacher_menu(users.Teacher(self.db))
            elif user_type == '4':
                self.student_menu(users.Student(self.db))
        except Exception as e:
            print(e)
    
    def admin_menu(self, admin):
        while True:
            print("\nАдминистраторское меню:")
            print("1: Добавить нового пользователя")
            print("2: Импорт новых пользователей")
            print("3: Добавить тест")
            print("4: Импорт тестов")
            print("5: Удалить пользователя")
            print("6: Редактировать пользователя")
            print("7: Создать группу")
            print("8: Заполнить группу")
            print("9: Добавить преподавателя в группу")
            print("10: Выход")
            choice = input("Выберите опцию: ")

            if choice == '1':
                admin.add_user()
            elif choice == '2':
                admin.import_users()
            elif choice == '3':
                admin.add_test()
            elif choice == '4':
                admin.import_tests()
            elif choice == '5':
                admin.delete_user()
            elif choice == '6':
                admin.edit_user()
            elif choice == '7':
                admin.create_group()
            elif choice == '8':
                admin.fill_group()
            elif choice == '9':
                admin.add_teacher_to_group()
            elif choice == '10':
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    def tutore_menu(self, tutore):
        while True:
            print("\nМеню куратора:")
            print("1: Создать группу")
            print("2: Заполнить группу")
            print("3: Добавить в группу преподавателя")
            print("4: Добавить/редактировать тесты")
            print("5: Просмотр результатов тестов")
            print("6: Выход")
            choice = input("Выберите опцию: ")

            if choice == '1':
                tutore.create_group()
            elif choice == '2':
                tutore.fill_group()
            elif choice == '3':
                tutore.add_teacher_to_group()
            elif choice == '4':
                tutore.manage_tests()
            elif choice == '5':
                tutore.view_test_results()
            elif choice == '6':
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    def teacher_menu(self, teacher):
        while True:
            print("\nМеню преподавателя:")
            print("1: Добавить тесты")
            print("2: Просмотр результатов тестов")
            print("3: Выход")
            choice = input("Выберите опцию: ")

            if choice == '1':
                teacher.add_test()
            elif choice == '2':
                teacher.view_test_results()
            elif choice == '3':
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    def student_menu(self, student):
        while True:
            print("\nМеню ученика:")
            print("1: Прохождение тестов")
            print("2: Выход")
            choice = input("Выберите опцию: ")

            if choice == '1':
                student.take_test()
            elif choice == '2':
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")
