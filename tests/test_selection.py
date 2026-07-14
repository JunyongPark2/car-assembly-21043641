from parts import CarType, EngineType, BrakeType, SteeringType
from selection import CarSelection


def test_new_selection_starts_empty():
    selection = CarSelection()
    assert selection.car_type is None
    assert selection.engine is None
    assert selection.brake is None
    assert selection.steering is None


def test_set_car_type_stores_enum_and_returns_it():
    selection = CarSelection()
    result = selection.set_car_type(2)
    assert result == CarType.SUV
    assert selection.car_type == CarType.SUV


def test_set_engine_stores_enum_and_returns_it():
    selection = CarSelection()
    result = selection.set_engine(4)
    assert result == EngineType.BROKEN
    assert selection.engine == EngineType.BROKEN


def test_set_brake_stores_enum_and_returns_it():
    selection = CarSelection()
    result = selection.set_brake(3)
    assert result == BrakeType.BOSCH
    assert selection.brake == BrakeType.BOSCH


def test_set_steering_stores_enum_and_returns_it():
    selection = CarSelection()
    result = selection.set_steering(1)
    assert result == SteeringType.BOSCH
    assert selection.steering == SteeringType.BOSCH


def test_selections_are_independent_instances():
    a = CarSelection()
    b = CarSelection()
    a.set_car_type(1)
    assert a.car_type == CarType.SEDAN
    assert b.car_type is None
