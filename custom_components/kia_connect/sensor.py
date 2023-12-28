"""Sensor to read vehicle data from Kia Connected Services"""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry


from homeassistant.const import (
    PERCENTAGE
)
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.components.sensor.const import UnitOfPressure, UnitOfTime
from homeassistant.core import HomeAssistant

from .KiaConnectEntity import KiaConnectEntity
from .KiaConnectVehicle import KiaConnectVehicle

from .const import DISTANCE_UNITS, DOMAIN, DRIVING_STYLES, KIA_CONNECT_VEHICLE, PROPULSION_BEV, PROPULSION_PHEV, PROPULSION_ICE, VEHICLE_TIRES

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Kia vehicle sensors"""

    vehicle: KiaConnectVehicle = hass.data[DOMAIN][config_entry.entry_id][KIA_CONNECT_VEHICLE]
    sensors = []

    if vehicle.propulsion == PROPULSION_BEV or vehicle.propulsion == PROPULSION_PHEV:
        sensors.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "ev_charge_level",
                "EV Charge Level",
                "evInfo.chargeLevel",
                PERCENTAGE,
                None,
                SensorDeviceClass.BATTERY,
                SensorStateClass.MEASUREMENT
            )
        )
        sensors.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "ev_charge_time_remaining",
                "EV Charge Time Remaining",
                "evInfo.timeUntilCharged",
                UnitOfTime.MINUTES,
                "mdi:battery-clock",
                SensorDeviceClass.DURATION,
                SensorStateClass.MEASUREMENT
            )
        )
    
    #elif vehicle.propulsion == PROPULSION_ICE:
        #TODO Add combustion engine sensors

    sensors.append(
        VehicleSensor(
            hass,
            config_entry,
            vehicle,
            "odometer",
            "Odometer",
            "odoMeter",
            DISTANCE_UNITS,
            "mdi:gauge",
            SensorDeviceClass.DISTANCE,
            SensorStateClass.TOTAL
        )
    )
    
    sensors.append(
        VehicleSensor(
            hass,
            config_entry,
            vehicle,
            "range",
            "Range",
            "range",
            DISTANCE_UNITS,
            "mdi:gauge",
            SensorDeviceClass.DISTANCE,
            SensorStateClass.MEASUREMENT
        )
    )

    for driving_style in DRIVING_STYLES:
        sensors.append(
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
                SensorStateClass.MEASUREMENT
            )
        )
    
    for tire in VEHICLE_TIRES:
        sensors.append(
            VehicleSensor(
                hass,
                config_entry,
                vehicle,
                "tire_pressure_{}".format(tire["key"]),
                "Tire Pressure {}".format(tire["name"]),
                "tirePressures.{}".format(tire["key"]),
                UnitOfPressure.BAR,
                "mdi:tire",
                SensorDeviceClass.PRESSURE,
                SensorStateClass.MEASUREMENT
            )
        )
    async_add_entities(sensors)
    


class VehicleSensor(KiaConnectEntity, SensorEntity):
    def __init__(
        self,
        hass,
        config_entry,
        vehicle: KiaConnectVehicle,
        id,
        name,
        key,
        unit,
        icon,
        device_class: SensorDeviceClass,
        state_class: SensorStateClass,
    ):
        super().__init__(hass, config_entry, vehicle, name)
        self._id = id

        self._key = key
        self.vehicle = vehicle

        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_device_class = device_class
        self._attr_state_class = state_class

    @property
    def native_value(self):
        return self.vehicle.get_child_value(self._key)

    @property
    def available(self) -> bool:
        return self.vehicle.get_child_value(self._key) is not None

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self.vehicle.vin}-{self._id}"
