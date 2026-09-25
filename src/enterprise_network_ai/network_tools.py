from typing import Any

from .data import devices as DEVICES


def _get_device(device_id: str) -> dict[str, Any]:
    """
    Return a network device from the simulated inventory.

    Args:
        device_id: Unique network device identifier.

    Raises:
        ValueError: If the device does not exist.
    """

    device = DEVICES.get(device_id)

    if not device:
        raise ValueError(
            f"Device '{device_id}' was not found."
        )

    return device


def get_device_status(
    device_id: str,
) -> dict[str, Any]:
    """
    Get the operational status and resource utilization
    of a network device.

    Args:
        device_id: Unique device identifier.
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


def get_device_alerts(
    device_id: str,
) -> dict[str, Any]:
    """
    Get active alerts for a network device.

    Args:
        device_id: Unique device identifier.
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
    Get the operational state, traffic and error
    information for a specific interface.

    Args:
        device_id: Unique device identifier.
        interface_name: Interface name such as
            GigabitEthernet0/0.
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


def get_bgp_neighbors(
    device_id: str,
) -> dict[str, Any]:
    """
    Get BGP neighbor state for a network device.

    Args:
        device_id: Unique device identifier.
    """

    device = _get_device(device_id)

    return {
        "device_id": device_id,
        "neighbors": device["bgp_neighbors"],
    }