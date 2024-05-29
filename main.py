import database
import ui

if __name__ == '__main__':
    db = database.DataBase()
    ui_app = ui.UI(db)
