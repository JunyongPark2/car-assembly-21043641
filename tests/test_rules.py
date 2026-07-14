import pytest

from parts import CarType, EngineType, BrakeType, SteeringType
from selection import CarSelection
from rules import find_violations


def _selection(car_type, engine, brake, steering):
    return CarSelection(car_type=car_type, engine=engine, brake=brake, steering=steering)


def test_no_violations_for_fully_compatible_combo():
    selection = _selection(CarType.SEDAN, EngineType.GM, BrakeType.MANDO, SteeringType.BOSCH)
    assert find_violations(selection) == []


@pytest.mark.parametrize(
    "car_type, engine, brake, steering, expected_message",
    [
        (
            CarType.SEDAN, EngineType.GM, BrakeType.CONTINENTAL, SteeringType.BOSCH,
            "Sedan에는 Continental제동장치 사용 불가",
        ),
        (
            CarType.SUV, EngineType.TOYOTA, BrakeType.MANDO, SteeringType.BOSCH,
            "SUV에는 TOYOTA엔진 사용 불가",
        ),
        (
            CarType.TRUCK, EngineType.WIA, BrakeType.CONTINENTAL, SteeringType.BOSCH,
            "Truck에는 WIA엔진 사용 불가",
        ),
        (
            CarType.TRUCK, EngineType.GM, BrakeType.MANDO, SteeringType.BOSCH,
            "Truck에는 Mando제동장치 사용 불가",
        ),
        (
            CarType.SEDAN, EngineType.GM, BrakeType.BOSCH, SteeringType.MOBIS,
            "Bosch제동장치에는 Bosch조향장치 이외 사용 불가",
        ),
    ],
)
def test_single_rule_violation_reports_its_message(
    car_type, engine, brake, steering, expected_message
):
    selection = _selection(car_type, engine, brake, steering)
    assert find_violations(selection) == [expected_message]


def test_multiple_violations_are_all_reported_in_rule_order():
    # Truck + Mando (rule 4) and Truck + WIA (rule 3) both apply; rule order
    # in COMPATIBILITY_RULES should be preserved in the result.
    selection = _selection(CarType.TRUCK, EngineType.WIA, BrakeType.MANDO, SteeringType.BOSCH)
    violations = find_violations(selection)
    assert violations == [
        "Truck에는 WIA엔진 사용 불가",
        "Truck에는 Mando제동장치 사용 불가",
    ]
