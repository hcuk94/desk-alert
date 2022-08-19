#!/usr/bin/python -u
import sys
import datetime
import logging
from mod import database
import config
from mod import emailer
from mod import gobright
from time import sleep
import requests

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)-15s %(levelname)-8s %(message)s")


if __name__ == "__main__":
    logging.info("Program Started.")
    db_driver = database.Database()
    gb_driver = gobright.GoBright()
    while True:
        logging.info("Starting checks...")
        pending_checks = db_driver.checks_pending()

        for check in pending_checks:
            (check_id, check_datetime, check_duration) = check

            # Verify whether the entry has expired
            datetime_obj = datetime.datetime.strptime(check_datetime, '%Y-%m-%d %H:%M')
            datetime_exp = datetime_obj + datetime.timedelta(hours=config.expire_check_after_hours)
            if datetime.datetime.utcnow() > datetime_exp:
                db_driver.expire_check(check[0])

            # Check Availability
            else:
                num_avail = gb_driver.num_desks(check_datetime, check_duration)
                if num_avail >= 1:
                    print(f"A desk was found on {check_datetime}!")
                    db_driver.fulfill_check(check_id)

        sleep(config.seconds_to_sleep)



