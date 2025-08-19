# virtual_iot.py
# This code simulates a MicroPython IoT device that reads temperature and humidity data
# and sends the data to a FastAPI server. It is designed to run on a regular
from time import sleep
import requests  # For making HTTP requests
import json      # For formatting our data as JSON
import random    # For simulating sensor data


class DHT22(object):
    def __init__(self, pin):
        self.pin = pin

    def measure(self):
        # Simulate measuring temperature and humidity
        self.temp = 18 + random.random() * 17  # Random temp between 20-30
        self.hum = 40 + random.random() * 40     # Random humidity between 30-80

    def temperature(self):
        return self.temp

    def humidity(self):
        return self.hum

sensor = DHT22(pin=6)  # Simulated sensor object

SERVER_IP = "192.168.0.9"  # <-- CHANGE THIS TO YOUR ACTUAL COMPUTER'S IP ADDRESS
SERVER_URL = f"http://{SERVER_IP}:8000/sensor_data"
HEADERS = {'Content-Type': 'application/json'}

# --- MAIN LOOP ---
while True:
    try:
        # 1. Read the sensor data
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f"Reading: Temp={temp:.2f}°C, Hum={hum:.2f}%")

        # 2. Prepare the data payload
        payload = {
            "temperature": temp,
            "humidity": hum
        }

        # Convert the dictionary to a JSON string
        json_data = json.dumps(payload)

        # 3. Send the data to the server
        print(f"Sending data to {SERVER_URL}...")
        response = requests.post(SERVER_URL, headers=HEADERS, data=json_data)
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Wait for 10 seconds before sending the next reading
    sleep(10)