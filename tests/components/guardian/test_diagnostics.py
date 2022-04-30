"""Test Guardian diagnostics."""
from homeassistant.components.diagnostics import REDACTED
from homeassistant.components.guardian import (
    DATA_PAIRED_SENSOR_MANAGER,
    DOMAIN,
    PairedSensorManager,
)

from tests.components.diagnostics import get_diagnostics_for_config_entry


async def test_entry_diagnostics(hass, config_entry, hass_client, setup_guardian):
    """Test config entry diagnostics."""
    paired_sensor_manager: PairedSensorManager = hass.data[DOMAIN][
        config_entry.entry_id
    ][DATA_PAIRED_SENSOR_MANAGER]

    # Simulate the pairing of a paired sensor:
    await paired_sensor_manager.async_pair_sensor("AABBCCDDEEFF")

    assert await get_diagnostics_for_config_entry(hass, hass_client, config_entry) == {
        "entry": {
            "title": "Mock Title",
            "data": {
                "ip_address": "192.168.1.100",
                "port": 7777,
                "uid": REDACTED,
            },
        },
        "data": {
            "valve_controller": {
                "sensor_pair_dump": {"pair_count": 1, "paired_uids": REDACTED},
                "system_diagnostics": {
                    "codename": "gvc1",
                    "uid": REDACTED,
                    "uptime": 41,
                    "firmware": "0.20.9-beta+official.ef3",
                    "rf_modem_firmware": "4.0.0",
                    "available_heap": 34456,
                },
                "system_onboard_sensor_status": {"temperature": 71, "wet": False},
                "valve_status": {
                    "enabled": False,
                    "direction": True,
                    "state": 0,
                    "travel_count": 0,
                    "instantaneous_current": 0,
                    "instantaneous_current_ddt": 0,
                    "average_current": 34,
                },
                "wifi_status": {
                    "station_connected": True,
                    "ip_assigned": True,
                    "mqtt_connected": True,
                    "rssi": -63,
                    "channel": 1,
                    "lan_ipv4": "192.168.1.100",
                    "lan_ipv6": "AC10:BD0:FFFF:FFFF:AC10:BD0:FFFF:FFFF",
                    "ap_enabled": True,
                    "ap_clients": 0,
                    "bssid": REDACTED,
                    "ssid": REDACTED,
                },
            },
            "paired_sensors": [
                {
                    "uid": REDACTED,
                    "codename": "gld1",
                    "temperature": 68,
                    "wet": False,
                    "moved": True,
                    "battery_percentage": 79,
                }
            ],
        },
    }
