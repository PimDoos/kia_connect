"""Constants for the Kia Connected Services integration."""
from homeassistant.components.sensor.const import UnitOfLength

# Configuration
DOMAIN = "kia_connect"

CONF_API_ENDPOINT = "api_endpoint"

API_ENDPOINT_NL = "https://mijnkia.nl/api"
API_ENDPOINTS = [ API_ENDPOINT_NL ]

API_FIELDS_VEHICLE_ID = [ "houderschapsId" ]

API_PATH_USER = "/user"
API_PATH_USER_LOGIN = "/user/login"
API_PATH_USER_LOGGED_IN = "/user/is-logged-in"
API_PATH_USER_LOGOUT = "/user/logout"
API_PATH_VEHICLE_STATUS = "/vehicle/{id}/connected-status"

DATA_VEHICLE_LISTENER = "vehicle_listener"

DEFAULT_SCAN_INTERVAL = 60
DEVICE_MANUFACTURER = "Kia"

DRIVING_STYLE_ECO = "eco"
DRIVING_STYLE_NORMAL = "normal"
DRIVING_STYLE_SPORT = "sport"

DRIVING_STYLES = [
	DRIVING_STYLE_ECO,
	DRIVING_STYLE_NORMAL,
	DRIVING_STYLE_SPORT
]

VEHICLE_TIRES = [ 
	{"key": "frontLeft", "name":"Front Left"},
	{"key": "frontRight", "name":"Front Right"},
	{"key": "rearLeft", "name":"Rear Left"},
	{"key": "rearRight", "name":"Rear Right"},
]

DISTANCE_UNITS = UnitOfLength.KILOMETERS

KIA_CONNECT_API = "kia_connect_api"
KIA_CONNECT_VEHICLE = "kia_connect_vehicle"

PROPULSION_BEV = "BEV"
PROPULSION_PHEV = "PHEV"
PROPULSION_ICE = "ICE"

TOPIC_UPDATE: str = f"{DOMAIN}_update_{0}"

MAX_UPDATE_RETRY_COUNT = 3
