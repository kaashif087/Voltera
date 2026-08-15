from context.devices.device_type import DeviceType


def test_valid_device_types():
    assert DeviceType.LAPTOP.value == "laptop"
    assert DeviceType.PHONE.value == "phone"
    assert DeviceType.TABLET.value == "tablet"
    assert DeviceType.WATCH.value == "watch"
    assert DeviceType.UNKNOWN.value == "unknown"


def test_device_type_from_value():
    assert DeviceType.from_value("laptop") == DeviceType.LAPTOP
    assert DeviceType.from_value("phone") == DeviceType.PHONE
    assert DeviceType.from_value("tablet") == DeviceType.TABLET
    assert DeviceType.from_value("watch") == DeviceType.WATCH
    assert DeviceType.from_value("unknown") == DeviceType.UNKNOWN


def test_device_type_from_value_is_case_insensitive():
    assert DeviceType.from_value("LAPTOP") == DeviceType.LAPTOP
    assert DeviceType.from_value("Phone") == DeviceType.PHONE
    assert DeviceType.from_value("TABLET") == DeviceType.TABLET
    assert DeviceType.from_value("Watch") == DeviceType.WATCH


def test_device_type_from_value_strips_whitespace():
    assert DeviceType.from_value(" laptop ") == DeviceType.LAPTOP
    assert DeviceType.from_value("  phone") == DeviceType.PHONE
    assert DeviceType.from_value("tablet  ") == DeviceType.TABLET


def test_valid_device_type_detection():
    assert DeviceType.is_valid("laptop")
    assert DeviceType.is_valid("phone")
    assert DeviceType.is_valid("tablet")
    assert DeviceType.is_valid("watch")
    assert DeviceType.is_valid("unknown")


def test_invalid_device_type_detection():
    assert not DeviceType.is_valid("desktop")
    assert not DeviceType.is_valid("television")
    assert not DeviceType.is_valid("")
    assert not DeviceType.is_valid("computer")


def test_invalid_device_type_values():
    invalid_values = [
        "desktop",
        "television",
        "",
        "computer",
    ]

    for value in invalid_values:
        try:
            DeviceType.from_value(value)
            raise AssertionError(
                f"Expected ValueError for invalid value: {value!r}"
            )
        except ValueError:
            pass


def test_non_string_values_are_rejected():
    invalid_values = [
        None,
        123,
        3.14,
        [],
        {},
    ]

    for value in invalid_values:
        assert DeviceType.is_valid(value) is False

        try:
            DeviceType.from_value(value)
            raise AssertionError(
                f"Expected TypeError for value: {value!r}"
            )
        except TypeError:
            pass


def test_value_string():
    assert DeviceType.LAPTOP.value_string == "laptop"
    assert DeviceType.PHONE.value_string == "phone"
    assert DeviceType.TABLET.value_string == "tablet"
    assert DeviceType.WATCH.value_string == "watch"
    assert DeviceType.UNKNOWN.value_string == "unknown"


def test_all_device_types_are_unique():
    values = [device_type.value for device_type in DeviceType]

    assert len(values) == len(set(values))


def run_test(name, test_function):
    try:
        test_function()
        print(f"{name:<50} -> PASS")
        return True
    except Exception as error:
        print(f"{name:<50} -> FAIL")
        print(f"    {error}")
        return False


if __name__ == "__main__":
    results = [
        run_test(
            "Valid Device Types",
            test_valid_device_types,
        ),
        run_test(
            "Device Type From Value",
            test_device_type_from_value,
        ),
        run_test(
            "Case Insensitive Conversion",
            test_device_type_from_value_is_case_insensitive,
        ),
        run_test(
            "Whitespace Handling",
            test_device_type_from_value_strips_whitespace,
        ),
        run_test(
            "Valid Device Type Detection",
            test_valid_device_type_detection,
        ),
        run_test(
            "Invalid Device Type Detection",
            test_invalid_device_type_detection,
        ),
        run_test(
            "Invalid Device Type Values",
            test_invalid_device_type_values,
        ),
        run_test(
            "Non-String Values Rejected",
            test_non_string_values_are_rejected,
        ),
        run_test(
            "Value String",
            test_value_string,
        ),
        run_test(
            "Device Type Uniqueness",
            test_all_device_types_are_unique,
        ),
    ]

    passed = sum(results)
    total = len(results)

    print()
    print(f"Phase 5.3 Device Type Tests: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)