import sqlite3
from os.path import exists


class Database:
    def __init__(self):
        self.db_name = 'desk-alert.db'
        if exists(self.db_name):
            self.db = sqlite3.connect(self.db_name)
        else:
            self.db = sqlite3.connect(self.db_name)
            self.db_setup()

    def db_setup(self):
        default_config = [
            ("seconds_to_sleep", "300"),
            ("expire_check_after_hours", "2"),
            ("email_from", "example@example.com"),
            ("email_to", "example@example.com"),
            ("email_server", "localhost")
        ]

        cur = self.db.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS CHECKS
            (ID INTEGER PRIMARY KEY,
            DATETIME TEXT NOT NULL,
            DURATION INT NOT NULL,
            FULFILLED TEXT)
        """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS CONFIG
                    (KEY TEXT PRIMARY KEY NOT NULL,
                    VALUE TEXT NOT NULL)
                """)
        cur.executemany("INSERT INTO CONFIG (KEY, VALUE) VALUES(?,?)", default_config)
        cur.close()
        self.commit()

    def get_config(self, conf_key):
        cur = self.db.cursor()
        cur.execute("SELECT VALUE FROM CONFIG WHERE KEY = ?", (conf_key,))
        data = cur.fetchone()[0]
        cur.close()
        return data

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()

    def create_check(self, date_time, duration):
        cur = self.db.cursor()
        cur.execute("INSERT INTO CHECKS (DATETIME, DURATION, FULFILLED) VALUES(?, ?, 'P');", (date_time, duration,))
        cur.close()
        self.commit()

    def expire_check(self, check_id):
        cur = self.db.cursor()
        cur.execute("UPDATE CHECKS SET FULFILLED = 'N' WHERE ID = ?", (check_id,))
        cur.close()
        self.commit()

    def fulfill_check(self, check_id):
        cur = self.db.cursor()
        cur.execute("UPDATE CHECKS SET FULFILLED = 'Y' WHERE ID = ?", (check_id,))
        cur.close()
        self.commit()

    def checks_pending(self):
        cur = self.db.cursor()
        cur.execute("SELECT ID, DATETIME, DURATION FROM CHECKS WHERE FULFILLED = \'P\'")
        checks_data = cur.fetchall()
        cur.close()
        return checks_data
