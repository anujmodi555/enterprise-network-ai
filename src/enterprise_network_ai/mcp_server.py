import logging

from fastmcp import FastMCP

from enterprise_network_ai.network_tools import (
    get_bgp_neighbors as network_get_bgp_neighbors,
    get_device_alerts as network_get_device_alerts,
    get_device_status as network_get_device_status,
    get_interface_status as network_get_interface_status,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


mcp = FastMCP(
    name="Enterprise Network Tools",
)


@mcp.tool
def get_device_status(
    device_id: str,
) -> dict:
    """
    Get the current operational status, CPU utilization,
    memory utilization, vendor and model of a network device.

    Args:
        device_id: Unique device identifier such as R1.
    """

    logger.info(
        "MCP tool called: get_device_status device=%s",
        device_id,
    )

    return network_get_device_status(device_id)


@mcp.tool
def get_device_alerts(
    device_id: str,
) -> dict:
    """
    Get active alerts for a network device.

    Args:
        device_id: Unique device identifier such as R1.
    """

    logger.info(
        "MCP tool called: get_device_alerts device=%s",
        device_id,
    )

    return network_get_device_alerts(device_id)


@mcp.tool
def get_interface_status(
    device_id: str,
    interface_name: str,
) -> dict:
    """
    Get operational state, traffic and error information
    for a specific network interface.

    Args:
        device_id: Unique device identifier such as R1.
        interface_name: Interface name such as
            GigabitEthernet0/0.
    """

    logger.info(
        "MCP tool called: get_interface_status "
        "device=%s interface=%s",
        device_id,
        interface_name,
    )

    return network_get_interface_status(
        device_id=device_id,
        interface_name=interface_name,
    )


@mcp.tool
def get_bgp_neighbors(
    device_id: str,
) -> dict:
    """
    Get BGP neighbor state for a network device.

    Args:
        device_id: Unique device identifier such as R1.
    """

    logger.info(
        "MCP tool called: get_bgp_neighbors device=%s",
        device_id,
    )

    return network_get_bgp_neighbors(device_id)


if __name__ == "__main__":
    mcp.run()