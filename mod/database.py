import sqlite3
import datetime

class Database:
    def __init__(self):
        self.db_name = 'database.db'
        db = sqlite3.connect(self.db_name)

        db.execute("""
            CREATE TABLE IF NOT EXISTS CHECKS
            (ID INT PRIMARY KEY NOT NULL,
            DATETIME TEXT NOT NULL,
            DURATION INT NOT NULL,
            FULFILLED CHAR(1);
        """)
        db.close()

    def create_check(self, date_time, duration):
        db = sqlite3.connect(self.db_name)

        db.execute(f"INSERT INTO CHECKS (DATETIME, DURATION) VALUES ({date_time}, {duration});")

        db.close()

    def checks_unfulfilled(self):
        db = sqlite3.connect(self.db_name)

        checks = db.execute("SELECT ID, DATETIME, DURATION FROM CHECKS"
                            "WHERE FULFILLED = 'P'")

        for check in checks:
            dt_str = check[1]
            dt_obj = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
            dt_exp = dt_obj + datetime.timedelta(0, 7200)
            if dt_obj < dt_exp:
