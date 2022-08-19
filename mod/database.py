import sqlite3
import datetime


class Database:
    def __init__(self):
        self.db_name = 'desk-alert.db'
        self.db = sqlite3.connect(self.db_name)
        cur = self.db.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS CHECKS
            (ID INTEGER PRIMARY KEY,
            DATETIME TEXT NOT NULL,
            DURATION INT NOT NULL,
            FULFILLED TEXT)
        """)
        cur.close()
        self.commit()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()

    def create_check(self, date_time, duration):
        cur = self.db.cursor()
        cur.execute(f"INSERT INTO CHECKS (DATETIME, DURATION, FULFILLED) VALUES(\'{date_time}\', {duration}, 'P');")
        cur.close()
        self.commit()

    def expire_check(self, check_id):
        cur = self.db.cursor()
        cur.execute(f"UPDATE CHECKS SET FULFILLED = 'N' WHERE ID = {check_id}")
        cur.close()
        self.commit()

    def fulfill_check(self, check_id):
        cur = self.db.cursor()
        cur.execute(f"UPDATE CHECKS SET FULFILLED = 'Y' WHERE ID = {check_id}")
        cur.close()
        self.commit()

    def checks_pending(self):
        cur = self.db.cursor()
        cur.execute("SELECT ID, DATETIME, DURATION FROM CHECKS WHERE FULFILLED = \'P\'")
        checks_data = cur.fetchall()
        cur.close()
        return checks_data
