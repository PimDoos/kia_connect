"""MyKia API wrapper """
import logging
import aiohttp

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
        api_base_uri: str
    ):
        self.username = username
        self.password = password
        self.api_base_uri = api_base_uri
        self.user = {}
        self.vehicle = {}
        self.session = aiohttp.ClientSession()

    async def login(self) -> bool:
        """Authenticates the API session using the credentials specified in the constructor"""

        payload = {
            "username": self.username,
            "password": self.password
        }
        url = self.api_base_uri + API_PATH_USER_LOGIN
        async with self.session.post(url, json=payload) as response:
            if(response.status == 200):
                api_response = await response.json()
                if api_response["isSuccess"]:
                    self.user = await self.get_user()
                    return True
                else:
                    return False
            else:
                return False

    async def logout(self) -> bool:
        """Deauthenticates the API session"""
        url = self.api_base_uri + API_PATH_USER_LOGOUT
        async with self.session.get(url) as response:
            if(response.status == 200):
                api_response = await response.json()
                if api_response["isSuccess"]:
                    return True
                else:
                    return False
            else:
                return False

    async def is_logged_in(self) -> bool:
        """Checks whether the session is currently authenticated"""
        url = self.api_base_uri + API_PATH_USER_LOGGED_IN
        async with self.session.get(url) as response:
            if(response.status == 200):
                api_response = await response.json()
                return api_response["isSuccess"]
            else:
                return False

    async def get_user(self):
        """Get the currently logged in user"""
        url = self.api_base_uri + API_PATH_USER
        async with self.session.get(url) as response:
            if response.status == 200:
                api_response = await response.json()
                if api_response["isSuccess"]:
                    user = api_response["data"]
                return user
            else:
                return None

    async def get_vehicle_ids(self):
        """Get a list of vehicle IDs associated with the logged in user"""
        vehicle_ids = []

        for vehicle in self.user["vehicles"]:
            for id_field_name in API_FIELDS_VEHICLE_ID:
                if vehicle[id_field_name]:
                    vehicle_ids.append(vehicle[id_field_name])
                    break
        
        return vehicle_ids

    async def get_preferred_vehicle_id(self):
        return self.user["preferredVehicle"]

    async def get_vehicle_info(self, vehicle_id: int):
        if self.user is not None:
            for vehicle in self.user["vehicles"]:
                for id_field_name in API_FIELDS_VEHICLE_ID:
                    if vehicle[id_field_name] == vehicle_id:
                        return vehicle

            return None
        else:
            return None


    async def get_vehicle_status(self, vehicle_id: int):
        """Get the vehicle status"""
        url = self.api_base_uri + API_PATH_VEHICLE_STATUS.format(id=vehicle_id)
        async with self.session.get(url) as response:
            if response.status == 200:
                api_response = await response.json()
                if api_response["isSuccess"]:
                    
                    vehicle = api_response["data"]
                    return vehicle
                else:
                    return None
            else:
                return None
