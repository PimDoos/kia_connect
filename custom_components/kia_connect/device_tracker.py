"""Sensor to read vehicle data from Kia Connected Services"""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.components.device_tracker.const import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .KiaConnectEntity import KiaConnectEntity
from .KiaConnectVehicle import KiaConnectVehicle

from .const import DOMAIN, KIA_CONNECT_VEHICLE

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the Kia vehicle sensors"""

    vehicle = hass.data[DOMAIN][config_entry.entry_id][KIA_CONNECT_VEHICLE]
    tracker = VehicleTracker(hass, config_entry, vehicle)
    async_add_entities([tracker])
    


class VehicleTracker(KiaConnectEntity, TrackerEntity):
    def __init__(
        self,
        hass,
        config_entry,
        vehicle: KiaConnectVehicle,
    ):
        super().__init__(hass, config_entry, vehicle, "Location")
        self.vehicle = vehicle
        self._attr_icon = "mdi:map-marker"
        self._source_type = SourceType.GPS

    @property
    def latitude(self):
        return self.vehicle.get_child_value("position.latitude")

    @property
    def longitude(self):
        return self.vehicle.get_child_value("position.longitude")

    @property
    def source_type(self):
        return self._source_type

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self.vehicle.vin}-tracker"
