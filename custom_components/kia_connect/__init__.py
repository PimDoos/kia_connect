"""The Kia Connected Services integration."""
from __future__ import annotations
from datetime import timedelta
import datetime
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from homeassistant.helpers.event import async_track_time_interval

from homeassistant.util import dt as dt_util

from .const import DATA_VEHICLE_LISTENER, DEFAULT_SCAN_INTERVAL, DOMAIN, KIA_CONNECT_API, KIA_CONNECT_VEHICLE, CONF_API_ENDPOINT
from .KiaConnectApi import KiaConnectApi
from .KiaConnectVehicle import KiaConnectVehicle

_LOGGER = logging.getLogger(__name__)

# TODO Reduce this to 1 before submitting to HA Core.
PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.DEVICE_TRACKER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Kia Connected Services from a config entry."""

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN][KIA_CONNECT_API] = KiaConnectApi(
        username = config_entry.data.get(CONF_USERNAME),
        password = config_entry.data.get(CONF_PASSWORD),
        api_base_uri = config_entry.data.get(CONF_API_ENDPOINT),
    )
    login_success = await hass.async_add_executor_job(
        hass.data[DOMAIN][KIA_CONNECT_API].login
    )
    if not login_success:
        raise ConfigEntryAuthFailed

    vehicle_id = await hass.async_add_executor_job(
        hass.data[DOMAIN][KIA_CONNECT_API].get_preferred_vehicle_id
    )
    hass.data[DOMAIN][KIA_CONNECT_VEHICLE] = KiaConnectVehicle(
        hass, 
        config_entry, 
        hass.data[DOMAIN][KIA_CONNECT_API], 
        vehicle_id
    )
    scan_interval = timedelta(
        seconds=DEFAULT_SCAN_INTERVAL
    )

    async def update(event_time_utc: datetime):
        await hass.async_add_executor_job(
            hass.data[DOMAIN][KIA_CONNECT_VEHICLE].update_status
        )
    
    await update(dt_util.utcnow())
    hass.data[DOMAIN][DATA_VEHICLE_LISTENER] = async_track_time_interval(hass, update, scan_interval)

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        hass.data[DOMAIN][KIA_CONNECT_VEHICLE] = None

        await hass.async_add_executor_job(
            hass.data[DOMAIN][KIA_CONNECT_API].logout
        )

    return unload_ok
