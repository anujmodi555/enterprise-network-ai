from pydantic import BaseModel


class DeviceStatus(BaseModel):
    hostname: str
    vendor: str
    model: str
    status: str
    cpu: float
    memory: float


class Alert(BaseModel):
    severity: str
    message: str