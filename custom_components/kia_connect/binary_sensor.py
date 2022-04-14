"""Sensor to read vehicle data from Kia Connected Services"""
from __future__ import annotations
from typing import Any
from homeassistant.config_entries import ConfigEntry


from homeassistant.const import (
    STATE_OFF,
    STATE_ON
)
from homeassistant.components.binary_sensor import DEVICE_CLASS_BATTERY_CHARGING, DEVICE_CLASS_LOCK, DEVICE_CLASS_PLUG, BinarySensorEntity
from homeassistant.core import HomeAssistant

from .KiaConnectEntity import KiaConnectEntity
from .KiaConnectVehicle import KiaConnectVehicle

from .const import DOMAIN, KIA_CONNECT_VEHICLE, PROPULSION_BEV, PROPULSION_PHEV, PROPULSION_ICE

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Kia vehicle sensors"""

    vehicle = hass.data[DOMAIN][KIA_CONNECT_VEHICLE]
    VEHICLE_SENSORS = []

    if vehicle.propulsion == PROPULSION_BEV or vehicle.propulsion == PROPULSION_PHEV:
        VEHICLE_SENSORS.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "ev_charging",
                "EV Charging",
                "evInfo.isCharging",
                None,
                None,
                DEVICE_CLASS_BATTERY_CHARGING
            )
        )
        VEHICLE_SENSORS.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "ev_plugged",
                "EV Plugged In",
                "evInfo.isPlugged",
                None,
                None,
                DEVICE_CLASS_PLUG
            )
        )
    #elif vehicle.propulsion == PROPULSION_ICE:
        #TODO Add combustion engine sensors

    VEHICLE_SENSORS.append(
        VehicleSensor(
            hass,
            config_entry,
            vehicle,
            "doors_unlocked",
            "Door Locks",
            "doorsLocked",
            "mdi:car-door",
            "mdi:car-door-lock",
            DEVICE_CLASS_LOCK,
            True
        )
    )
    VEHICLE_SENSORS.append(
        VehicleSensor(
            hass,
            config_entry,
            vehicle,
            "handbrake",
            "Handbrake",
            "handbrake",
            "mdi:car-brake-parking",
            "mdi:car-brake-parking",
            None
        )
    )

    async_add_entities(VEHICLE_SENSORS)
    


class VehicleSensor(KiaConnectEntity, BinarySensorEntity):
    def __init__(
        self,
        hass,
        config_entry,
        vehicle: KiaConnectVehicle,
        id,
        description,
        key,
        icon_on,
        icon_off,
        device_class,
        invert = False
    ):
        super().__init__(hass, config_entry, vehicle)
        self._id = id
        self._description = description
        self._key = key
        self._icon_on = icon_on
        self._icon_off = icon_off
        self._device_class = device_class
        self.vehicle = vehicle
        self._invert = invert

    @property
    def is_on(self) -> bool:
        value = bool(self.vehicle.get_child_value(self._key))
        if self._invert:
            return not value
        else:
            return value

    @property
    def state(self):
        if self.is_on:
            return STATE_ON
        else:
            return STATE_OFF

    @property
    def icon(self):
        if self.is_on:
            return self._icon_on
        else:
            return self._icon_off

    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self):
        return f"{self.vehicle.name} {self._description}"

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self.vehicle.vin}-{self._id}"