# Copy this file to config.py and fill in your values.
# config.py is gitignored — never commit real credentials.

# WiFi
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# Node-RED base station
SERVER_BASE_URL = "http://192.168.x.x:1880"
SEND_DATA_URL = SERVER_BASE_URL + "/endpoint/wstn/readings"
GET_CONFIG_URL = SERVER_BASE_URL + "/endpoint/wstn/config"

# Default sleep interval between readings (seconds)
MAIN_SLEEP = 10

# Logging
LOG_ENABLED = True
LOG_FILE = "weather.log"
