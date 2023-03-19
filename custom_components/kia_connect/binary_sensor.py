"""Sensor to read vehicle data from Kia Connected Services"""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry


from homeassistant.const import (
    STATE_OFF,
    STATE_ON
)
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import HomeAssistant

from .KiaConnectEntity import KiaConnectEntity
from .KiaConnectVehicle import KiaConnectVehicle

from .const import DOMAIN, KIA_CONNECT_VEHICLE, PROPULSION_BEV, PROPULSION_PHEV, PROPULSION_ICE, VEHICLE_TIRES

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Kia vehicle sensors"""

    vehicle = hass.data[DOMAIN][config_entry.entry_id][KIA_CONNECT_VEHICLE]
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
                BinarySensorDeviceClass.BATTERY_CHARGING
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
                BinarySensorDeviceClass.PLUG
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
            BinarySensorDeviceClass.LOCK,
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
            "mdi:car-brake-alert",
            None
        )
    )

    for tire in VEHICLE_TIRES:
        VEHICLE_SENSORS.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "tire_warning_{}".format(tire["key"]),
                "Tire Warning {}".format(tire["name"]),
                "tireWarnings.{}".format(tire["key"]),
                "mdi:car-tire-alert",
                "mdi:tire",
                BinarySensorDeviceClass.PROBLEM
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
        name,
        key,
        icon_on,
        icon_off,
        device_class,
        invert = False
    ):
        super().__init__(hass, config_entry, vehicle, name)
        self._id = id
        self._key = key
        self._icon_on = icon_on
        self._icon_off = icon_off
        self._attr_device_class = device_class
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
    def available(self) -> bool:
        return self.vehicle.get_child_value(self._key) is not None

    @property
    def icon(self):
        if self.is_on:
            return self._icon_on
        else:
            return self._icon_off

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self.vehicle.vin}-{self._id}"
