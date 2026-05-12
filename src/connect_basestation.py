import urequests
import ujson
import network
import time
import config
from logger import log


def connect_basestation(voltage, rpm, main_sleep, temperature, pressure, humidity, rainguage_count, sample_duration_s=None):
    data = {
        "temp": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "volts": voltage,
        "rpm": rpm,
        "rainguageCount": rainguage_count
    }
    headers = {"Content-Type": "application/json"}

    log("Payload: {}".format(ujson.dumps(data)))

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    log("WLAN interface activated")

    if not wlan.isconnected():
        log("Not connected. Connecting to WiFi SSID='{}'...".format(config.WIFI_SSID))
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            log("Waiting for WiFi... {}s remaining".format(timeout))
            time.sleep(1)
            timeout -= 1
    else:
        log("WiFi already connected")

    if wlan.isconnected():
        ifconfig = wlan.ifconfig()
        log("WiFi connected: IP={}, subnet={}, gateway={}, dns={}".format(*ifconfig))
    else:
        log("WiFi connection failed after timeout. Aborting send.")
        wlan.active(False)
        return main_sleep, sample_duration_s

    if sample_duration_s is None:
        sample_duration_s = config.WINDSPEED_SAMPLING_SIZE

    try:
        log("GET config from: {}".format(config.GET_CONFIG_URL))
        response = urequests.get(config.GET_CONFIG_URL)
        log("GET config response status: {}".format(response.status_code))

        header_value = response.headers.get("main_sleep")
        if header_value:
            old_sleep = main_sleep
            main_sleep = float(header_value)
            log("main_sleep updated from {}s to {}s via response header".format(
                old_sleep, main_sleep))
        else:
            log("No 'main_sleep' header in config response. Keeping {}s".format(main_sleep))

        sampling_header = response.headers.get("windspeed_sampling_size")
        if sampling_header:
            old_sample = sample_duration_s
            sample_duration_s = float(sampling_header)
            log("sample_duration_s updated from {}s to {}s via response header".format(
                old_sample, sample_duration_s))
        else:
            log("No 'windspeed_sampling_size' header in config response. Keeping {}s".format(sample_duration_s))
        response.close()

        payload_str = ujson.dumps(data)
        log("POST data to: {}".format(config.SEND_DATA_URL))
        log("POST body: {}".format(payload_str))
        response = urequests.post(
            config.SEND_DATA_URL,
            data=payload_str,
            headers=headers
        )
        log("POST response status: {}".format(response.status_code))
        response.close()

    except Exception as e:
        log("HTTP error: {} - {}".format(type(e).__name__, e))

    log("Deactivating WLAN interface")
    wlan.active(False)
    wlan.deinit()
    log("WLAN deactivated and deinitialized")

    return main_sleep, sample_duration_s
