"""The Kia Connected Services integration."""
from __future__ import annotations
from datetime import timedelta
import datetime
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from homeassistant.helpers.event import async_track_time_interval

from homeassistant.util import dt as dt_util

from .const import DATA_VEHICLE_LISTENER, DEFAULT_SCAN_INTERVAL, DOMAIN, KIA_CONNECT_API, KIA_CONNECT_VEHICLE, CONF_API_ENDPOINT
from .KiaConnectApi import KiaConnectApi
from .KiaConnectVehicle import KiaConnectVehicle

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.DEVICE_TRACKER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Kia Connected Services from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {}

    api = KiaConnectApi(
        username = config_entry.data.get(CONF_USERNAME),
        password = config_entry.data.get(CONF_PASSWORD),
        api_base_uri = config_entry.data.get(CONF_API_ENDPOINT)
    )
    login_success = await api.login()

    if not login_success:
        raise ConfigEntryAuthFailed
    
    hass.data[DOMAIN][config_entry.entry_id][KIA_CONNECT_API] = api

    vehicle_id = await api.get_preferred_vehicle_id()
    vehicle_info = await api.get_vehicle_info(vehicle_id)

    if not vehicle_info:
        raise ConfigEntryNotReady
        
    hass.data[DOMAIN][config_entry.entry_id][KIA_CONNECT_VEHICLE] = KiaConnectVehicle(
        hass, 
        config_entry, 
        api, 
        vehicle_id,
        vehicle_info
    )
    scan_interval = timedelta(
        seconds=DEFAULT_SCAN_INTERVAL
    )

    async def update(event_time_utc: datetime):
        await hass.data[DOMAIN][config_entry.entry_id][KIA_CONNECT_VEHICLE].update_status()
    
    await update(dt_util.utcnow())
    hass.data[DOMAIN][config_entry.entry_id][DATA_VEHICLE_LISTENER] = async_track_time_interval(hass, update, scan_interval)

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        entry_data = hass.data[DOMAIN][entry.entry_id]
        await entry_data[KIA_CONNECT_API].logout()

        if DATA_VEHICLE_LISTENER in entry_data:
            entry_data[DATA_VEHICLE_LISTENER]()

        hass.data[DOMAIN][entry.entry_id][KIA_CONNECT_VEHICLE] = None
        hass.data[DOMAIN][entry.entry_id][KIA_CONNECT_API] = None

        if entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id)
            
    return unload_ok
