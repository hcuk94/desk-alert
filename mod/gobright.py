import requests
import datetime


class GoBright:
    """Hello!"""
    def __init__(self, api_auth, location_id, date_time, duration):
        self.api_baseurl = "https://t1b.gobright.cloud/api/v2.0/"
        self.api_auth = api_auth
        self.location_id = location_id
        self.date_time = date_time
        self.duration = duration * 60

    def availability(self):
        req_url = self.api_baseurl + "spaces/desks/availability"
        req_head = {
            'Authorization': self.api_auth
        }
        req_body = {
              "timeZone": "Europe/London",
              "locationId": self.location_id,
              "dateTime": self.date_time,
              "duration": self.duration,
              "spaceType": 1,
              "capacity": 1,
        }
        req = requests.post(req_url, headers=req_head, json=req_body)
        req_resp = req.json()
        return req_resp

    def num_desks(self):
        avail = self.availability()
        locations = avail['data']['locations']
        count_loc = len(locations)
        count_desk = 0
        if count_loc > 0:
            for location in locations:
                count_desk += len(location['spaces'])
        return count_desk

