from __future__ import annotations

from context.devices.device import Device
from context.devices.device_type import DeviceType


class DeviceRegistry:
    """
    Central registry for all devices known to VOLTERA.

    The registry is intentionally device-type agnostic.
    It can manage laptops, phones, tablets, watches, and
    future device types without modification.
    """

    def __init__(self) -> None:
        self._devices: dict[str, Device] = {}

    def register(self, device: Device) -> None:
        """
        Register a device.

        Raises:
            TypeError: If the supplied object is not a Device.
            ValueError: If a device with the same ID is already registered.
        """
        if not isinstance(device, Device):
            raise TypeError("Only Device objects can be registered.")

        if device.device_id in self._devices:
            raise ValueError(
                f"Device already registered: {device.device_id!r}"
            )

        self._devices[device.device_id] = device

    def unregister(self, device_id: str) -> Device:
        """
        Remove and return a registered device.

        Raises:
            TypeError: If device_id is not a string.
            KeyError: If the device is not registered.
        """
        self._validate_device_id(device_id)

        if device_id not in self._devices:
            raise KeyError(
                f"Device is not registered: {device_id!r}"
            )

        return self._devices.pop(device_id)

    def get(self, device_id: str) -> Device | None:
        """
        Retrieve a device by ID.

        Returns:
            The Device object if found, otherwise None.
        """
        self._validate_device_id(device_id)
        return self._devices.get(device_id)

    def contains(self, device_id: str) -> bool:
        """
        Return True if a device is registered.
        """
        self._validate_device_id(device_id)
        return device_id in self._devices

    def count(self) -> int:
        """Return the number of registered devices."""
        return len(self._devices)

    def list_devices(self) -> list[Device]:
        """
        Return all registered devices.

        A new list is returned so callers cannot directly modify
        the registry's internal collection.
        """
        return list(self._devices.values())

    def get_by_type(self, device_type: DeviceType) -> list[Device]:
        """
        Return all devices matching a device type.

        Raises:
            TypeError: If device_type is not a DeviceType.
        """
        if not isinstance(device_type, DeviceType):
            raise TypeError(
                "device_type must be a DeviceType."
            )

        return [
            device
            for device in self._devices.values()
            if device.device_type == device_type
        ]

    def clear(self) -> None:
        """Remove all registered devices."""
        self._devices.clear()

    def _validate_device_id(self, device_id: str) -> None:
        """
        Validate a device ID.
        """
        if not isinstance(device_id, str):
            raise TypeError("Device ID must be a string.")

        if not device_id.strip():
            raise ValueError("Device ID cannot be empty.")