from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .KiaConnectVehicle import KiaConnectVehicle
from .const import DEVICE_MANUFACTURER, DOMAIN, KIA_CONNECT_VEHICLE, TOPIC_UPDATE


class KiaConnectEntity(Entity):
    def __init__(self, hass: HomeAssistant, config_entry, vehicle: KiaConnectVehicle):
        self.hass = hass
        self.config_entry = config_entry
        self.vehicle = vehicle
        self.topic_update = TOPIC_UPDATE.format(vehicle.id)
        self.topic_update_listener = None

    async def async_added_to_hass(self):
        @callback
        def update():
            self.update_from_latest_data()
            self.async_write_ha_state()

        await super().async_added_to_hass()
        self.topic_update_listener = async_dispatcher_connect(
            self.hass, self.topic_update, update
        )
        self.async_on_remove(self.topic_update_listener)
        self.update_from_latest_data()

    @property
    def available(self) -> bool:
        if not self.vehicle:
            return False
        elif not self.vehicle.info:
            return False
        elif not self.vehicle.data:
            return False
        else:
            return True

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.vehicle.vin)},
            "name": self.vehicle.name,
            "manufacturer": DEVICE_MANUFACTURER,
            "model": self.vehicle.model,
            "hw_version": self.vehicle.info["version"]
        }
    @callback
    def update_from_latest_data(self):
        self.vehicle = self.hass.data[DOMAIN][KIA_CONNECT_VEHICLE]
