devices = {
    "R1": {
        "hostname": "R1",
        "vendor": "Cisco",
        "model": "ASR1001-X",
        "status": "up",
        "cpu": 91,
        "memory": 62,
        "interfaces": {
            "GigabitEthernet0/0": {
                "status": "up",
                "errors": 0,
                "traffic_in": 820,
                "traffic_out": 740,
            },
            "GigabitEthernet0/1": {
                "status": "up",
                "errors": 2,
                "traffic_in": 420,
                "traffic_out": 390,
            },
        },
        "bgp_neighbors": {
            "10.0.0.2": "established",
            "10.0.0.3": "established",
        },
        "alerts": [
            {
                "severity": "warning",
                "message": "CPU utilization above 85%",
            }
        ],
    }
}