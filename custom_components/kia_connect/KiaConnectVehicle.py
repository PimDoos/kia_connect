"""Represents a Kia Connected Vehicle"""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from .KiaConnectApi import KiaConnectApi
from .const import DEVICE_MANUFACTURER, TOPIC_UPDATE

_LOGGER = logging.getLogger(__name__)

class KiaConnectVehicle:
    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        kia_api: KiaConnectApi,
        vehicle_id: int
    ):
        self.hass = hass
        self.config_entry: ConfigEntry = config_entry
        self.kia_api: KiaConnectApi = kia_api
        self.data = {}
        self.vehicle_id = vehicle_id
        self.topic_update = TOPIC_UPDATE.format(self.vehicle_id)
        self.info = {}

    
    def update_status(self):
        if not self.kia_api.is_logged_in():
            _LOGGER.debug("Refreshing Kia login info")
            self.kia_api.login()

        self.info = self.kia_api.get_vehicle_info(
            self.vehicle_id
        )
        self.data = self.kia_api.get_vehicle_status(
            self.vehicle_id
        )
        async_dispatcher_send(self.hass, self.topic_update)

    def get_status(self):
        if self.data:
            return None
        else:
            return self.data


    def get_child_value(self, key):
        value = self.data
        for node in key.split("."):
            try:
                value = value[node]
            except:
                try:
                    value = value[int(value)]
                except:
                    value = None
        return value

    @property
    def id(self):
        return self.vehicle_id
    
    @property
    def model(self):
        return self.info["model"]

    @property
    def name(self):
        return f"{DEVICE_MANUFACTURER} {self.model}"

    @property
    def vin(self):
        return self.info["vin"]

    @property
    def license_plate(self):
        return self.info["licensePlate"]

    @property
    def propulsion(self):
        return self.info["fuel"]

    
