"""MyKia API wrapper """
import logging
import requests
import json
from .const import (
    API_PATH_USER_LOGIN, 
    API_PATH_USER_LOGGED_IN,
    API_PATH_USER_LOGOUT,
    API_PATH_USER,
    API_PATH_VEHICLE_STATUS,
    API_FIELDS_VEHICLE_ID
)

_LOGGER = logging.getLogger(__name__)

class KiaConnectApi:
    def __init__(
        self,
        username: str,
        password: str,
        api_base_uri: str,
    ):
        self.username = username
        self.password = password
        self.api_base_uri = api_base_uri
        self.user = {}
        self.vehicle = {}

    def login(self) -> bool:
        """Authenticates the API session using the credentials specified in the constructor"""

        payload = {
            "username": self.username,
            "password": self.password
        }
        url = self.api_base_uri + API_PATH_USER_LOGIN
        response = requests.post(url, json=payload)
        self.cookies = response.cookies

        if(response.status_code == 200):
            api_response = json.loads(response.content)
            if api_response["isSuccess"]:
                self.user = self.get_user()
                return True
            else:
                return False
        else:
            return False

    def logout(self) -> bool:
        """Deauthenticates the API session"""
        url = self.api_base_uri + API_PATH_USER_LOGOUT
        response = requests.get(url)

        if(response.status_code == 200):
            api_response = json.loads(response.content)
            if api_response["isSuccess"]:
                return True
            else:
                return False
        else:
            return False

    def is_logged_in(self) -> bool:
        """Checks whether the session is currently authenticated"""
        url = self.api_base_uri + API_PATH_USER_LOGGED_IN
        response = requests.get(url, cookies=self.cookies)
        if(response.status_code == 200):
            api_response = json.loads(response.content)
            if api_response["isSuccess"]:
                self.cookies.update(response.cookies)
                return True
            else:
                return False
        else:
            return False

    def get_user(self):
        """Get the currently logged in user"""
        url = self.api_base_uri + API_PATH_USER
        response = requests.get(url, cookies=self.cookies)
        api_response = json.loads(response.content)
        if response.status_code == 200:
            user = api_response["data"]
            return user
        else:
            return None

    def get_vehicle_ids(self):
        """Get a list of vehicle IDs associated with the logged in user"""
        vehicle_ids = []

        for vehicle in self.user["vehicles"]:
            for id_field_name in API_FIELDS_VEHICLE_ID:
                if vehicle[id_field_name]:
                    vehicle_ids.append(vehicle[id_field_name])
                    break
        
        return vehicle_ids

    def get_preferred_vehicle_id(self):
        return self.user["preferredVehicle"]

    def get_vehicle_info(self, vehicle_id: int):
        self.user = self.get_user()

        for vehicle in self.user["vehicles"]:
            for id_field_name in API_FIELDS_VEHICLE_ID:
                if vehicle[id_field_name] == vehicle_id:
                    return vehicle

        return None    


    def get_vehicle_status(self, vehicle_id: int):
        """Get the vehicle status"""
        url = self.api_base_uri + API_PATH_VEHICLE_STATUS.format(id=vehicle_id)
        response = requests.get(url, cookies=self.cookies)
        api_response = json.loads(response.content)

        if response.status_code == 200:
            vehicle = api_response["data"]
            return vehicle
        else:
            return None
