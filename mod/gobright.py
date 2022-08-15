import requests


class GoBright:
    """Hello!"""
    def __init__(self, api_endpoint, api_auth):
        self.api_endpoint = api_endpoint
        self.api_auth = api_auth

    def availability(self):
        req_url = self.api_endpoint + "spaces/desks/availability"
        req_head = {
            'Authorization': self.api_auth
        }
        req_body = {
              "timeZone": "Europe/London",
              "locationId": "bb0527a8-0c37-4580-bdac-092c7df2249d",
              "dateTime": "2022-08-18 08:00",
              "duration": 480,
              "spaceType": 1,
              "capacity": 1,
        }
        req = requests.post(req_url, headers=req_head, json=req_body)
        req_resp = req.json()
        return req_resp
