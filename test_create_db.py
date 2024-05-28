import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    ID         INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    Name       TEXT    NOT NULL,
    TypeOfUser TEXT    NOT NULL,
    Login      TEXT    NOT NULL
                       UNIQUE,
    Password   TEXT    NOT NULL,
    FOREIGN KEY (
        TypeOfUser
    )
    REFERENCES TypeOfUsers (Code) ON DELETE NO ACTION
                                  ON UPDATE CASCADE,
    UNIQUE (
        ID
    )
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS TypeOfUsers (
    Code        INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    Description TEXT    NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Tests (
    Code             INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    Name             TEXT    NOT NULL,
    Creator          INTEGER NOT NULL,
    [Group]          INTEGER NOT NULL
                             REFERENCES [Group] (Code) ON DELETE NO ACTION
                                                       ON UPDATE CASCADE,
    NumberOfAttempts INTEGER NOT NULL,
    FOREIGN KEY (
        Creator
    )
    REFERENCES Users (ID) 
);
''')

cursor.execute('''
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

cursor.execute('''
CREATE TABLE IF NOT EXISTS TeachersGroups (
    IDTeacher INTEGER REFERENCES Users (ID) ON DELETE NO ACTION
                                            ON UPDATE CASCADE,
    CodeGroup INTEGER REFERENCES [Group] (Code) ON DELETE NO ACTION
                                                ON UPDATE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions (
    Code        INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    Description TEXT    NOT NULL,
    CodeTest    INTEGER NOT NULL,
    FOREIGN KEY (
        CodeTest
    )
    REFERENCES Tests (Code) 
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS [Group] (
    Code      INTEGER PRIMARY KEY ASC AUTOINCREMENT
                      UNIQUE
                      NOT NULL,
    NameGroup TEXT    NOT NULL
                      UNIQUE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS BandMembers (
    CodeGroup INTEGER REFERENCES [Group] (Code) ON DELETE NO ACTION
                                                ON UPDATE CASCADE,
    IDStudent INTEGER REFERENCES Users (ID) ON DELETE NO ACTION
                                            ON UPDATE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Answers (
    Code          INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    Description   TEXT    NOT NULL,
    Accuracy      BOOLEAN NOT NULL,
    CodeQuestions INTEGER NOT NULL,
    FOREIGN KEY (
        CodeQuestions
    )
    REFERENCES Questions (Code) 
);
''')