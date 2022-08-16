#!/usr/bin/python -u
import config
from mod import emailer
from mod import gobright
import logging
from time import sleep
import requests

date_time = "2022-08-16 08:00"
duration = 8

test = gobright.GoBright(config.gb_auth, config.gb_location, date_time, duration)
print(test.num_desks())
