from fastapi import FastAPI, HTTPException

from .data import devices
from .models import DeviceStatus, Alert


app = FastAPI(
    title="Enterprise Network Simulator",
    version="1.0.0",
)


@app.get("/devices/{device_id}/status", response_model=DeviceStatus)
def get_device_status(device_id: str):
    device = devices.get(device_id)

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device


@app.get("/devices/{device_id}/alerts", response_model=list[Alert])
def get_device_alerts(device_id: str):
    device = devices.get(device_id)

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device["alerts"]