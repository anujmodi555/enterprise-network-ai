from .data import devices as DEVICES


def build_network_context(device_id: str) -> str:
    """
    Convert network device information into
    text that can be provided to the LLM.
    """

    device = DEVICES.get(device_id)

    if not device:
        raise ValueError(f"Device '{device_id}' not found.")

    return f"""
Device ID: {device_id}
Hostname: {device["hostname"]}
Vendor: {device["vendor"]}
Model: {device["model"]}
Status: {device["status"]}
CPU utilization: {device["cpu"]}%
Memory utilization: {device["memory"]}%

Interfaces:
{device["interfaces"]}

BGP neighbors:
{device["bgp_neighbors"]}

Alerts:
{device["alerts"]}
"""