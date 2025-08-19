# Obtronics Agricultural Temperature and Humidity Sensor Beacon

This project is a Python-based application for the simulation of a real world sensor placed on various agricultural fields to measure the real time temperature and humidity of that field.

## Features

- FastAPI server for RESTful API
- Real-time data processing

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn beacon_iot_server:app --host 0.0.0.0 --port 8000
```

## Usage

Access the API at [http://<server_ip>:8000](http://<server_ip>:8000).

## Find the Server IP Address


```bash
ipconfig
```
