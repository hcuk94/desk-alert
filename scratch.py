#!/usr/bin/python -u
import sys

import config
from mod import emailer
from mod import gobright
import logging
from time import sleep
import requests

date_time = "2022-08-19 08:00"
duration = 8

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)-15s %(levelname)-8s %(message)s")

logging.info("Hello!")
test = gobright.GoBright()

while True:
    num_avail = test.num_desks(date_time, duration)
    if num_avail is not None:
        print(num_avail)
    sleep(60)
