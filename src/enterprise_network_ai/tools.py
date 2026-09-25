from typing import Any

from .data import devices as DEVICES


def _get_device(device_id: str) -> dict[str, Any]:
    """
    Retrieve a device from the simulated network inventory.

    Raises:
        ValueError: If the device does not exist.
    """

    device = DEVICES.get(device_id)

    if not device:
        raise ValueError(
            f"Device '{device_id}' was not found."
        )

    return device


def get_device_status(device_id: str) -> dict[str, Any]:
    """
    Get the current operational status and resource utilization
    of a network device.

    Args:
        device_id: Unique identifier of the network device.

    Returns:
        Dictionary containing device status, CPU and memory utilization.
    """

    device = _get_device(device_id)

    return {
        "device_id": device_id,
        "hostname": device["hostname"],
        "vendor": device["vendor"],
        "model": device["model"],
        "status": device["status"],
        "cpu": device["cpu"],
        "memory": device["memory"],
    }


def get_device_alerts(device_id: str) -> dict[str, Any]:
    """
    Get active alerts for a network device.

    Args:
        device_id: Unique identifier of the network device.

    Returns:
        Dictionary containing the device alerts.
    """

    device = _get_device(device_id)

    return {
        "device_id": device_id,
        "alerts": device["alerts"],
    }


def get_interface_status(
    device_id: str,
    interface_name: str,
) -> dict[str, Any]:
    """
    Get operational details for a specific network interface.

    Args:
        device_id: Unique identifier of the network device.
        interface_name: Interface name such as GigabitEthernet0/0.

    Returns:
        Interface operational status and traffic/error information.
    """

    device = _get_device(device_id)

    interface = device["interfaces"].get(interface_name)

    if interface is not None:
        return {
            "device_id": device_id,
            "interface": {
                "name": interface_name,
                **interface,
            },
        }

    raise ValueError(
        f"Interface '{interface_name}' was not found "
        f"on device '{device_id}'."
    )


def get_bgp_neighbors(device_id: str) -> dict[str, Any]:
    """
    Get BGP neighbor state for a network device.

    Args:
        device_id: Unique identifier of the network device.

    Returns:
        Dictionary containing BGP neighbor information.
    """

    device = _get_device(device_id)

    return {
        "device_id": device_id,
        "neighbors": device["bgp_neighbors"],
    }


TOOL_REGISTRY = {
    "get_device_status": get_device_status,
    "get_device_alerts": get_device_alerts,
    "get_interface_status": get_interface_status,
    "get_bgp_neighbors": get_bgp_neighbors,
}


TOOL_DECLARATIONS = [
    {
        "name": "get_device_status",
        "description": (
            "Get the current operational status, CPU utilization, "
            "memory utilization, vendor and model of a network device."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "device_id": {
                    "type": "string",
                    "description": (
                        "Unique device identifier, for example R1."
                    ),
                }
            },
            "required": ["device_id"],
        },
    },
    {
        "name": "get_device_alerts",
        "description": (
            "Get active alerts for a network device."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "device_id": {
                    "type": "string",
                    "description": (
                        "Unique device identifier, for example R1."
                    ),
                }
            },
            "required": ["device_id"],
        },
    },
    {
        "name": "get_interface_status",
        "description": (
            "Get status, errors and traffic information for "
            "a specific network interface."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "device_id": {
                    "type": "string",
                    "description": (
                        "Unique device identifier, for example R1."
                    ),
                },
                "interface_name": {
                    "type": "string",
                    "description": (
                        "Interface name, for example "
                        "GigabitEthernet0/0."
                    ),
                },
            },
            "required": [
                "device_id",
                "interface_name",
            ],
        },
    },
    {
        "name": "get_bgp_neighbors",
        "description": (
            "Get the BGP neighbor state and details for a "
            "network device."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "device_id": {
                    "type": "string",
                    "description": (
                        "Unique device identifier, for example R1."
                    ),
                }
            },
            "required": ["device_id"],
        },
    },
]