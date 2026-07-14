import pytest

from parts import CarType, EngineType, BrakeType, SteeringType


@pytest.mark.parametrize(
    "member, expected_label",
    [(CarType.SEDAN, "Sedan"), (CarType.SUV, "SUV"), (CarType.TRUCK, "Truck")],
)
def test_car_type_label(member, expected_label):
    assert member.label == expected_label


@pytest.mark.parametrize(
    "member, expected_label",
    [
        (EngineType.GM, "GM"),
        (EngineType.TOYOTA, "TOYOTA"),
        (EngineType.WIA, "WIA"),
        (EngineType.BROKEN, "고장난 엔진"),
    ],
)
def test_engine_type_label(member, expected_label):
    assert member.label == expected_label


@pytest.mark.parametrize(
    "member, expected_label",
    [
        (BrakeType.MANDO, "Mando"),
        (BrakeType.CONTINENTAL, "Continental"),
        (BrakeType.BOSCH, "Bosch"),
    ],
)
def test_brake_type_label(member, expected_label):
    assert member.label == expected_label


@pytest.mark.parametrize(
    "member, expected_label",
    [(SteeringType.BOSCH, "Bosch"), (SteeringType.MOBIS, "Mobis")],
)
def test_steering_type_label(member, expected_label):
    assert member.label == expected_label


@pytest.mark.parametrize(
    "enum_cls, value",
    [(CarType, 99), (EngineType, 99), (BrakeType, 99), (SteeringType, 99)],
)
def test_unknown_value_raises(enum_cls, value):
    with pytest.raises(ValueError):
        enum_cls(value)
