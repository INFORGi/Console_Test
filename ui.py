import users

class UI:
    def __init__(self, db):
        try:
            self.db = db
            user = self.db.verification_of_authorization()

            if user[2] == '1':
                admin = users.Admin()
            if user[2] == '2':
                admin = users.Tutore()
            if user[2] == '3':
                admin = users.Teacher()
            if user[2] == '4':
                admin = users.Student()
        except Exception as e:
            print(e)