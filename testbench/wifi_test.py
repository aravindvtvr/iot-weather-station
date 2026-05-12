import urequests
import ujson
import network
import time
import sys
from machine import ADC, Pin
import network
import machine


# ---------- WiFi credentials ----------
WIFI_SSID = "avsjaa_63"
WIFI_PASSWORD = "fraser274@2015"

# ---------- Server URL ----------
SEND_DATA_URL = "http://192.168.1.49:1880/endpoint/wstn/readings"

GET_CONFIG_URL = "http://192.168.1.49:1880/endpoint/wstn/config"
HEADER_NAME = "main_sleep"   # header you want to read
MAIN_SLEEP = 10
# ---------- Connect to WiFi ---------


# ---------- HTTP POST function ----------
def connect_basestation(voltage):
    data = {
        "temp": "50",
        "humidity": "55",
        "volts" : voltage 
    }

    headers = {
        "Content-Type": "application/json"
    }
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("WiFi connected:", wlan.ifconfig())
    else:
        print("WiFi failed")
        
    try:
        response = urequests.get(GET_CONFIG_URL)

        print("Status code:", response.status_code)

        # Read header value
        header_value = response.headers.get(HEADER_NAME)
        global MAIN_SLEEP
        MAIN_SLEEP = float(header_value)
        print(f"{HEADER_NAME} header:", MAIN_SLEEP)
        response.close()
        # Now lets send the sensor data to Base Station
        response = urequests.post(
            SEND_DATA_URL,
            data=ujson.dumps(data),
            headers=headers
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        response.close()
        

    except Exception as e:
        print("HTTP error:", e)
    wlan.active(False)
    wlan.deinit()

   


def get_vsys():
    import machine

    Vsys = machine.ADC(29)
    conversion_factor = (3.3 / (65535)) * 3
    reading = Vsys.read_u16() * conversion_factor
    print(reading)
    return reading

  
time.sleep(5)
# ---------- Infinite loop ----------
while True:
    print("starting")
    
    battery_voltage = get_vsys()
    connect_basestation(battery_voltage)
    print(f"sleeping for {MAIN_SLEEP}")
    time.sleep(MAIN_SLEEP)






