import json
import tempfile
from pathlib import Path

from context.devices.device_identity import DeviceIdentity


def test_device_id_exists():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "device_identity.json"

        identity = DeviceIdentity(storage_path)
        device_id = identity.get_or_create_id()

        assert device_id is not None
        assert isinstance(device_id, str)
        assert len(device_id) > 0


def test_device_id_is_valid():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "device_identity.json"

        identity = DeviceIdentity(storage_path)
        device_id = identity.get_or_create_id()

        assert DeviceIdentity.is_valid_id(device_id)


def test_device_id_remains_stable():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "device_identity.json"

        first_identity = DeviceIdentity(storage_path)
        first_id = first_identity.get_or_create_id()

        second_identity = DeviceIdentity(storage_path)
        second_id = second_identity.get_or_create_id()

        assert first_id == second_id


def test_different_storage_creates_different_ids():
    with tempfile.TemporaryDirectory() as temp_dir:
        first_path = Path(temp_dir) / "device_1.json"
        second_path = Path(temp_dir) / "device_2.json"

        first_identity = DeviceIdentity(first_path)
        second_identity = DeviceIdentity(second_path)

        first_id = first_identity.get_or_create_id()
        second_id = second_identity.get_or_create_id()

        assert first_id != second_id


def test_device_id_is_persisted():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "device_identity.json"

        identity = DeviceIdentity(storage_path)
        device_id = identity.get_or_create_id()

        assert storage_path.exists()

        with storage_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        assert data["device_id"] == device_id


def test_invalid_id_is_rejected():
    assert DeviceIdentity.is_valid_id("invalid-device-id") is False
    assert DeviceIdentity.is_valid_id("") is False
    assert DeviceIdentity.is_valid_id(None) is False
    assert DeviceIdentity.is_valid_id(12345) is False


def run_test(name, test_function):
    try:
        test_function()
        print(f"{name:<50} -> PASS")
        return True
    except Exception as error:
        print(f"{name:<50} -> FAIL")
        print(f"    {error}")
        return False

def test_corrupted_identity_is_replaced():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "device_identity.json"

        with storage_path.open("w", encoding="utf-8") as file:
            json.dump(
                {"device_id": "corrupted-invalid-id"},
                file,
            )

        identity = DeviceIdentity(storage_path)
        device_id = identity.get_or_create_id()

        assert DeviceIdentity.is_valid_id(device_id)

        with storage_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        assert data["device_id"] == device_id

if __name__ == "__main__":
    results = [
        run_test("Device ID Exists", test_device_id_exists),
        run_test("Device ID Is Valid", test_device_id_is_valid),
        run_test(
            "Device ID Remains Stable",
            test_device_id_remains_stable,
        ),
        run_test(
            "Different Storage Creates Different IDs",
            test_different_storage_creates_different_ids,
        ),
        run_test(
            "Device ID Is Persisted",
            test_device_id_is_persisted,
        ),
        run_test(
            "Invalid ID Is Rejected",
            test_invalid_id_is_rejected,
        ),
        run_test(
            "Corrupted Identity Is Replaced",
            test_corrupted_identity_is_replaced,
        ),
    ]

    passed = sum(results)
    total = len(results)

    print()
    print(f"Phase 5.2 Device Identity Tests: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)
