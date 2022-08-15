#!/usr/bin/python -u
import config
from mod import emailer
from mod import gobright
import logging
from time import sleep
import requests

test = gobright.GoBright(config.gobright_api, config.auth_cookie)
print(test.availability())
