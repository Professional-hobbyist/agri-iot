# beacon_iot_server.py

# This code sets up a FastAPI server to receive sensor data from a MicroPython IoT device.
# It also provides endpoints for a web browser to view the latest data and set alert thresholds.

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse 

# --- Data Shape Definitions ---

# This is for the incoming sensor data.
class SensorData(BaseModel):
    temperature: float
    humidity: float

# This is for defining the shape of the threshold settings.
# When the browser sends new thresholds, they must look like this.
class Thresholds(BaseModel):
    temp_min: float
    temp_max: float
    hum_min: float
    hum_max: float

# --- Create the App
app = FastAPI()

# --- In-Memory "Database" ---

# Stores the last data point from the beacon IoT device.
latest_data = { "temperature": 0.0, "humidity": 0.0 }

# NEW: Stores the current alert thresholds. We give it some sane defaults.
alert_thresholds = {
    "temp_min": 18.0,
    "temp_max": 28.0,
    "hum_min": 30.0,
    "hum_max": 60.0,
}

# --- API Endpoints ---

# Endpoint for the Pico to send data
@app.post("/sensor_data")
async def receive_sensor_data(data: SensorData):
    global latest_data
    latest_data = data.model_dump() # Use model_dump() for modern Pydantic
    print(f"Received and stored: Temp={latest_data['temperature']}°C, Hum={latest_data['humidity']}%")
    return {"status": "success"}

# Endpoint for the browser to get the latest sensor reading
@app.get("/get_latest_data")
async def get_latest_data():
    return latest_data

# Endpoint for the browser to get the current thresholds
@app.get("/get_thresholds")
async def get_thresholds():
    return alert_thresholds

# Endpoint for the browser to SET new thresholds
@app.post("/set_thresholds")
async def set_thresholds(thresholds: Thresholds):
    global alert_thresholds
    # FastAPI and Pydantic have already validated the incoming data for us!
    alert_thresholds = thresholds.model_dump()
    print(f"Updated thresholds to: {alert_thresholds}")
    return {"status": "success", "thresholds": alert_thresholds}

# Endpoint to serve the main dashboard page
@app.get("/")
async def read_root():
    return FileResponse('index.html')