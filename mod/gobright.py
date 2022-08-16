import logging
import requests
import datetime
import json
from time import sleep
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class GoBright:
    def __init__(self):
        logging.debug("Creating GoBright class instance")
        self.api_baseurl = "https://t1b.gobright.cloud/"
        self.api_client = ""
        self.api_secret = ""
        self.api_auth = ""
        self.api_token = ""
        self.auth_expiry = datetime.datetime.utcnow() + datetime.timedelta(0, 300)
        self.location_id = ""
        self.auth()

    def auth(self):
        """Handle initial browser pop-up to authenticate user"""
        logging.debug("Starting GoBright auth pop-up")
        options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(options=options)
        browser.get("https://portal.gobright.cloud/login/")

        logging.debug("Waiting for login process to complete")
        ui.WebDriverWait(browser, 300).until(ec.presence_of_element_located((By.CLASS_NAME, "date-picker")))

        logging.debug("Obtaining credentials...")
        auth_data = browser.execute_script("return window.localStorage.getItem('ls.authorizationData');")
        result = json.loads(auth_data)
        self.api_client = result['clientId']
        self.api_secret = result['clientSecret']
        self.api_auth = result['refreshToken']
        self.api_token = result['token']
        self.location_id = result['detailsData']['SettingDefaultLocationId']

    def re_auth(self):
        """Re-authenticate user by refresh token once duration of auth is up"""
        logging.debug("Re-auth process started")
        req_url = self.api_baseurl + "token"
        req_head = {
            'Authorization': "1"
        }
        req_body = {
            "grant_type": "refresh_token",
            "client_id": self.api_client,
            "client_secret": self.api_secret,
            "refresh_token": self.api_auth
        }
        req = requests.post(req_url, headers=req_head, data=req_body)
        if req.status_code == 200:
            req_resp = req.json()
            # Set token & expiry time
            self.api_token = req_resp['access_token']
            self.api_auth = req_resp['refresh_token']
            secs_validity = req_resp['expires_in']
            time = datetime.datetime.utcnow()
            self.auth_expiry = time + datetime.timedelta(0, secs_validity - 30)
        else:
            logging.error("An error occurred when renewing auth")

    def is_auth(self):
        """Simply checks if auth period has lapsed"""
        if self.auth_expiry > datetime.datetime.utcnow():
            return True
        else:
            return False

    def availability(self, date_time, duration):
        """Return full availability for desk search"""
        if not self.is_auth():
            self.re_auth()
        req_url = self.api_baseurl + "api/v2.0/spaces/desks/availability"
        req_head = {
            'Authorization': "Bearer " + self.api_token
        }
        req_body = {
              "timeZone": "Europe/London",
              "locationId": self.location_id,
              "dateTime": date_time,
              "duration": duration * 60,
              "spaceType": 1,
              "capacity": 1,
        }
        try:
            req = requests.post(req_url, headers=req_head, json=req_body)
            req_resp = req.json()
            return req_resp
        except (ConnectionError, requests.exceptions.ConnectTimeout) as error:
            logging.error(f"API Communication error: {error}")
            return None

    def num_desks(self, date_time, duration):
        """Returns the number of available desks for a search criteria"""
        avail = self.availability(date_time, duration)
        if avail is not None:
            locations = avail['data']['locations']
            count_loc = len(locations)
            count_desk = 0
            if count_loc > 0:
                for location in locations:
                    count_desk += len(location['spaces'])
            return count_desk
        else:
            logging.error("An error occurred while retrieving availability.")
            return None

