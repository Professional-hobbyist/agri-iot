# This code is for a MicroPython IoT device that reads temperature and humidity
# from a DHT11 sensor and sends the data to a FastAPI server.
# It is designed to run on any microcontroller capable of running MicroPython.
# The Arduino nano ESP32 supports micropython it is more energy efficient as
# it supports sleep mode reducing the current drawn to a few microAmps.
# The Raspberry Pi Zero has a Linus bases OS that it has to run on a 1Ghz
# single core CPU. Needless to say it consumes a lot more power and not ideal
# for battery powered devices.
# This code won't run on a regular computer.

from machine import Pin
from time import sleep
from dht import DHT11
import network   # For Wi-Fi
import urequests # For making HTTP requests
import json      # For formatting our data as JSON
import secrets   # To store the password of the Wi-Fi

# --- HARDWARE SETUP ---
sensor = DHT11(Pin(6)) # create the sensor object to get readings
led = Pin("LED", Pin.OUT) # let user know wifi status.

# --- CONFIGURATION ---
# This MUST be the IP address of the computer running the FastAPI server!
SERVER_IP = "192.168.228.226" # <-- CHANGE THIS TO YOUR ACTUAL COMPUTER'S IP ADDRESS
SERVER_URL = f"http://{SERVER_IP}:8000/sensor_data"
HEADERS = {'Content-Type': 'application/json'}

# --- WIFI CONNECTION ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    # Connect to the Wi-Fi. Bliknk to show connecting in progress
    led.toggle()
    sleep(1)
    print(".")

print("\nWi-Fi Connected!")
print("Local IP:", wlan.ifconfig()[0])
led.on() # Solid LED means that a connection has been established

# --- MAIN LOOP ---
while True:
    try:
        # 1. Read the sensor data
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f"Reading: Temp={temp}°C, Hum={hum}%")
        
        # 2. Prepare the data payload
        payload = {
            "temperature": temp,
            "humidity": hum
        }
        
        # Convert the dictionary to a JSON string
        json_data = json.dumps(payload)

        # 3. Send the data to the server
        print(f"Sending data to {SERVER_URL}...")
        
        # Wrap in try/except because network requests can fail!
        try:
            response = urequests.post(SERVER_URL, headers=HEADERS, data=json_data)
            
            # Printing the server's response for debugging
            print("Server Response:", response.text)
            response.close()
            
        except OSError as e:
            print(f"Error sending data: {e}")

    except OSError as e:
        print(f"Error reading sensor: {e}")

    # Waiting 5 seconds for the next cycle
    print("Waiting 5 seconds...")
    sleep(5)

