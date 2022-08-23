#!/usr/bin/python -u
import sys
import datetime
import logging
from mod import database
from mod import emailer
from mod import gobright
from time import sleep

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)-15s %(levelname)-8s %(message)s")


if __name__ == "__main__":
    logging.info("Program Started.")
    db_driver = database.Database()
    gb_driver = gobright.GoBright()

    while True:
        # Load config into memory
        conf_sleep = int(db_driver.get_config("seconds_to_sleep"))
        conf_expire = int(db_driver.get_config("expire_check_after_hours"))
        conf_mail_from = db_driver.get_config("email_from")
        conf_mail_to = db_driver.get_config("email_to")
        conf_mail_svr = db_driver.get_config("email_server")

        logging.info("Starting checks...")
        pending_checks = db_driver.checks_pending()

        for check in pending_checks:
            (check_id, check_datetime, check_duration) = check
            check_datetime = datetime.datetime.fromisoformat(check_datetime)
            # Verify whether the entry has expired
            datetime_exp = check_datetime + datetime.timedelta(hours=conf_expire)
            if datetime.datetime.now(datetime_exp.tzinfo) > datetime_exp:
                db_driver.expire_check(check[0])

            # Check Availability
            else:
                avail = gb_driver.availability(check_datetime, check_duration)
                count_desk = 0
                first_avail_desk_id = ""
                if avail is not None:
                    locations = avail['data']['locations']
                    count_loc = len(locations)

                    # If there is availability, increment desk count and set first desk ID
                    if count_loc > 0:
                        for location in locations:
                            count_desk += len(location['spaces'])
                        first_avail_desk_id = avail['data']['locations'][0]['spaces'][0]['id']
                else:
                    logging.error("An error occurred while retrieving availability.")

                # If we found a desk, then book it!
                if count_desk >= 1 and len(first_avail_desk_id) > 1:
                    logging.info(f"Desk found for {check_datetime}")
                    desk_booking = gb_driver.book_desk(first_avail_desk_id, check_datetime, check_duration)
                    if desk_booking is not None:
                        logging.info(f"Booked desk for {check_datetime}")
                        subj = f"Desk booked: {check_datetime}"
                        body = f"I found a desk on {check_datetime}, and have booked it for you."
                        emailer.send_email(conf_mail_svr, conf_mail_to, conf_mail_from, subj, body)

                    # Handle any error booking the desk, email anyway
                    else:
                        logging.error(f"Error occurred when booking desk for {check_datetime}")
                        subj = f"Error booking desk: {check_datetime}"
                        body = f"I found a desk on {check_datetime}, but was unable to make the booking."
                        emailer.send_email(conf_mail_svr, conf_mail_to, conf_mail_from, subj, body)

                    db_driver.fulfill_check(check_id)

                else:
                    logging.info(f"No desk found for {check_datetime}")

        logging.info(f"Sleeping for {conf_sleep} seconds...")
        sleep(conf_sleep)



