"""Sensor to read vehicle data from Kia Connected Services"""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry


from homeassistant.const import (
    DEVICE_CLASS_PRESSURE,
    PERCENTAGE,
    DEVICE_CLASS_BATTERY,
    PRESSURE_BAR,
    TIME_MINUTES
)
from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT, STATE_CLASS_TOTAL, STATE_CLASS_TOTAL_INCREASING, SensorEntity
from homeassistant.core import HomeAssistant

from .KiaConnectEntity import KiaConnectEntity
from .KiaConnectVehicle import KiaConnectVehicle

from .const import DISTANCE_UNITS, DOMAIN, DRIVING_STYLES, KIA_CONNECT_VEHICLE, PROPULSION_BEV, PROPULSION_PHEV, PROPULSION_ICE, VEHICLE_TIRES

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
                "ev_charge_level",
                "EV Charge Level",
                "evInfo.chargeLevel",
                PERCENTAGE,
                None,
                DEVICE_CLASS_BATTERY,
                STATE_CLASS_MEASUREMENT
            )
        )
        VEHICLE_SENSORS.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "ev_charge_time_remaining",
                "EV Charge Time Remaining",
                "evInfo.timeUntilCharged",
                TIME_MINUTES,
                "mdi:battery-clock",
                None,
                STATE_CLASS_MEASUREMENT
            )
        )
    
    #elif vehicle.propulsion == PROPULSION_ICE:
        #TODO Add combustion engine sensors

    VEHICLE_SENSORS.append(
        VehicleSensor(
            hass,
            config_entry,
            vehicle,
            "odometer",
            "Odometer",
            "odoMeter",
            DISTANCE_UNITS,
            "mdi:gauge",
            None,
            STATE_CLASS_TOTAL
        )
    )
    
    VEHICLE_SENSORS.append(
        VehicleSensor(
            hass,
            config_entry,
            vehicle,
            "range",
            "Range",
            "range",
            DISTANCE_UNITS,
            "mdi:gauge",
            None,
            STATE_CLASS_MEASUREMENT
        )
    )

    for driving_style in DRIVING_STYLES:
        VEHICLE_SENSORS.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "driving_style_{}".format(driving_style),
                "Driving Style {}".format(driving_style),
                "drivingStyle.{}".format(driving_style),
                PERCENTAGE,
                "mdi:steering",
                None,
                STATE_CLASS_MEASUREMENT
            )
        )
    
    for tire in VEHICLE_TIRES:
        VEHICLE_SENSORS.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "tire_pressure_{}".format(tire["key"]),
                "Tire Pressure {}".format(tire["name"]),
                "tirePressures.{}".format(tire["key"]),
                PRESSURE_BAR,
                "mdi:tire",
                DEVICE_CLASS_PRESSURE,
                STATE_CLASS_MEASUREMENT
            )
        )
    async_add_entities(VEHICLE_SENSORS)
    


class VehicleSensor(KiaConnectEntity, SensorEntity):
    def __init__(
        self,
        hass,
        config_entry,
        vehicle: KiaConnectVehicle,
        id,
        description,
        key,
        unit,
        icon,
        device_class,
        state_class,
    ):
        super().__init__(hass, config_entry, vehicle)
        self._id = id
        self._description = description
        self._key = key
        self._unit = unit
        self._icon = icon
        self._device_class = device_class
        self._state_class = state_class
        self.vehicle = vehicle

    @property
    def state(self):
        return self.vehicle.get_child_value(self._key)

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def icon(self):
        return self._icon

    @property
    def device_class(self):
        return self._device_class

    @property
    def state_class(self):
        return self._state_class

    @property
    def name(self):
        return f"{self.vehicle.name} {self._description}"

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self.vehicle.vin}-{self._id}"
