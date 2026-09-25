import pytest

from enterprise_network_ai.tools import (
    get_bgp_neighbors,
    get_device_alerts,
    get_device_status,
    get_interface_status,
)


def test_get_device_status():

    result = get_device_status("R1")

    assert result["device_id"] == "R1"
    assert result["status"] == "up"
    assert result["cpu"] == 91
    assert result["memory"] == 62


def test_get_device_alerts():

    result = get_device_alerts("R1")

    assert result["device_id"] == "R1"
    assert len(result["alerts"]) > 0


def test_get_interface_status():

    result = get_interface_status(
        device_id="R1",
        interface_name="GigabitEthernet0/0",
    )

    assert result["device_id"] == "R1"
    assert (
        result["interface"]["name"]
        == "GigabitEthernet0/0"
    )


def test_get_bgp_neighbors():

    result = get_bgp_neighbors("R1")

    assert result["device_id"] == "R1"
    assert len(result["neighbors"]) == 2


def test_unknown_device():

    with pytest.raises(ValueError):
        get_device_status("R999")


def test_unknown_interface():

    with pytest.raises(ValueError):
        get_interface_status(
            device_id="R1",
            interface_name="GigabitEthernet99/99",
        )