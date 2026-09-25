from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .data import devices as DEVICES
from .gemini_mcp import ask_network_assistant
from .models import Alert, DeviceStatus


app = FastAPI(
    title="Enterprise Network AI Assistant",
    version="4.0.0",
)


class TroubleshootingRequest(BaseModel):
    device_id: str = Field(
        min_length=1,
        description="Network device identifier",
    )

    question: str = Field(
        min_length=3,
        description="Network troubleshooting question",
    )


class TroubleshootingResponse(BaseModel):
    device_id: str
    question: str
    answer: str


@app.get(
    "/devices/{device_id}/status",
    response_model=DeviceStatus,
)
def get_device_status(device_id: str):

    device = DEVICES.get(device_id)

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return {
        "device_id": device_id,
        "hostname": device["hostname"],
        "vendor": device["vendor"],
        "model": device["model"],
        "status": device["status"],
        "cpu": device["cpu"],
        "memory": device["memory"],
    }


@app.get(
    "/devices/{device_id}/alerts",
    response_model=list[Alert],
)
def get_device_alerts(device_id: str):

    device = DEVICES.get(device_id)

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device["alerts"]


@app.post(
    "/troubleshoot",
    response_model=TroubleshootingResponse,
)
async def troubleshoot(
    request: TroubleshootingRequest,
):

    if request.device_id not in DEVICES:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    question = (
        f"Investigate device {request.device_id}.\n"
        f"User question: {request.question}"
    )

    try:

        answer = await ask_network_assistant(
            question=question,
        )

        return TroubleshootingResponse(
            device_id=request.device_id,
            question=request.question,
            answer=answer,
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc