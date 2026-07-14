import pytest

from parts import CarType, EngineType, BrakeType, SteeringType
from selection import CarSelection
from assemble import (
    validate_range,
    select_car_type,
    select_engine,
    select_brake,
    select_steering,
    is_valid_check,
    run_produced_car,
    test_produced_car as check_produced_car,
)

SEDAN, SUV, TRUCK = CarType.SEDAN, CarType.SUV, CarType.TRUCK
GM, TOYOTA, WIA = EngineType.GM, EngineType.TOYOTA, EngineType.WIA
MANDO, CONTINENTAL, BOSCH_B = BrakeType.MANDO, BrakeType.CONTINENTAL, BrakeType.BOSCH
BOSCH_S, MOBIS = SteeringType.BOSCH, SteeringType.MOBIS


# ---------------------------------------------------------------------------
# validate_range
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ans", [1, 2, 3])
def test_validate_range_step0_accepts_1_to_3(ans):
    assert validate_range(0, ans) is None


@pytest.mark.parametrize("ans", [0, 4, -1])
def test_validate_range_step0_rejects_outside_1_to_3(ans):
    assert validate_range(0, ans) is not None


@pytest.mark.parametrize("ans", [0, 1, 2, 3, 4])
def test_validate_range_step1_accepts_0_to_4(ans):
    assert validate_range(1, ans) is None


@pytest.mark.parametrize("ans", [-1, 5])
def test_validate_range_step1_rejects_outside_0_to_4(ans):
    assert validate_range(1, ans) is not None


@pytest.mark.parametrize("ans", [0, 1, 2, 3])
def test_validate_range_step2_accepts_0_to_3(ans):
    assert validate_range(2, ans) is None


@pytest.mark.parametrize("ans", [-1, 4])
def test_validate_range_step2_rejects_outside_0_to_3(ans):
    assert validate_range(2, ans) is not None


@pytest.mark.parametrize("ans", [0, 1, 2])
def test_validate_range_step3_accepts_0_to_2(ans):
    assert validate_range(3, ans) is None


@pytest.mark.parametrize("ans", [-1, 3])
def test_validate_range_step3_rejects_outside_0_to_2(ans):
    assert validate_range(3, ans) is not None


@pytest.mark.parametrize("ans", [0, 1, 2])
def test_validate_range_step4_accepts_0_to_2(ans):
    assert validate_range(4, ans) is None


@pytest.mark.parametrize("ans", [-1, 3])
def test_validate_range_step4_rejects_outside_0_to_2(ans):
    assert validate_range(4, ans) is not None


# ---------------------------------------------------------------------------
# selection functions: they mutate a CarSelection and return a confirmation
# message (no direct I/O - Phase 4 moved printing to the app/adapter layer)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ans, expected_snippet",
    [(1, "Sedan"), (2, "SUV"), (3, "Truck")],
)
def test_select_car_type_sets_selection_and_returns_message(ans, expected_snippet):
    selection = CarSelection()
    message = select_car_type(selection, ans)
    assert selection.car_type == CarType(ans)
    assert expected_snippet in message


@pytest.mark.parametrize(
    "ans, expected_snippet",
    [(1, "GM"), (2, "TOYOTA"), (3, "WIA"), (4, "고장난 엔진")],
)
def test_select_engine_sets_selection_and_returns_message(ans, expected_snippet):
    selection = CarSelection()
    message = select_engine(selection, ans)
    assert selection.engine == EngineType(ans)
    assert expected_snippet in message


@pytest.mark.parametrize(
    "ans, expected_snippet",
    [(1, "MANDO"), (2, "CONTINENTAL"), (3, "BOSCH")],
)
def test_select_brake_sets_selection_and_returns_message(ans, expected_snippet):
    selection = CarSelection()
    message = select_brake(selection, ans)
    assert selection.brake == BrakeType(ans)
    assert expected_snippet in message


@pytest.mark.parametrize(
    "ans, expected_snippet",
    [(1, "BOSCH"), (2, "MOBIS")],
)
def test_select_steering_sets_selection_and_returns_message(ans, expected_snippet):
    selection = CarSelection()
    message = select_steering(selection, ans)
    assert selection.steering == SteeringType(ans)
    assert expected_snippet in message


# ---------------------------------------------------------------------------
# is_valid_check: compatibility rules between parts
# ---------------------------------------------------------------------------

def _selection(car_type, engine, brake, steering):
    return CarSelection(car_type=car_type, engine=engine, brake=brake, steering=steering)


def test_is_valid_check_true_for_fully_compatible_combo():
    assert is_valid_check(_selection(SEDAN, GM, MANDO, BOSCH_S)) is True


def test_is_valid_check_false_sedan_with_continental_brake():
    assert is_valid_check(_selection(SEDAN, GM, CONTINENTAL, BOSCH_S)) is False


def test_is_valid_check_false_suv_with_toyota_engine():
    assert is_valid_check(_selection(SUV, TOYOTA, MANDO, BOSCH_S)) is False


def test_is_valid_check_false_truck_with_wia_engine():
    assert is_valid_check(_selection(TRUCK, WIA, CONTINENTAL, BOSCH_S)) is False


def test_is_valid_check_false_truck_with_mando_brake():
    assert is_valid_check(_selection(TRUCK, GM, MANDO, BOSCH_S)) is False


def test_is_valid_check_false_bosch_brake_with_non_bosch_steering():
    assert is_valid_check(_selection(SEDAN, GM, BOSCH_B, MOBIS)) is False


def test_is_valid_check_true_bosch_brake_with_bosch_steering():
    assert is_valid_check(_selection(SEDAN, GM, BOSCH_B, BOSCH_S)) is True


# ---------------------------------------------------------------------------
# run_produced_car
# ---------------------------------------------------------------------------

def test_run_produced_car_incompatible_parts_does_not_run():
    message = run_produced_car(_selection(SEDAN, GM, CONTINENTAL, BOSCH_S))
    assert "자동차가 동작되지 않습니다" in message
    assert "자동차가 동작됩니다" not in message


def test_run_produced_car_broken_engine_does_not_move():
    message = run_produced_car(_selection(SEDAN, EngineType.BROKEN, MANDO, BOSCH_S))
    assert "엔진이 고장나있습니다" in message
    assert "자동차가 움직이지 않습니다" in message


def test_run_produced_car_valid_combo_prints_full_spec():
    message = run_produced_car(_selection(SEDAN, GM, MANDO, BOSCH_S))
    assert "Car Type : Sedan" in message
    assert "Engine   : GM" in message
    assert "Brake    : Mando" in message
    assert "Steering : Bosch" in message
    assert "자동차가 동작됩니다" in message


# ---------------------------------------------------------------------------
# test_produced_car
# ---------------------------------------------------------------------------

def test_produced_car_pass_for_compatible_combo():
    message = check_produced_car(_selection(SEDAN, GM, MANDO, BOSCH_S))
    assert "PASS" in message


def test_produced_car_fail_sedan_continental():
    message = check_produced_car(_selection(SEDAN, GM, CONTINENTAL, BOSCH_S))
    assert "FAIL" in message


def test_produced_car_fail_suv_toyota():
    message = check_produced_car(_selection(SUV, TOYOTA, MANDO, BOSCH_S))
    assert "FAIL" in message


def test_produced_car_fail_truck_wia():
    message = check_produced_car(_selection(TRUCK, WIA, CONTINENTAL, BOSCH_S))
    assert "FAIL" in message


def test_produced_car_fail_truck_mando():
    message = check_produced_car(_selection(TRUCK, GM, MANDO, BOSCH_S))
    assert "FAIL" in message


def test_produced_car_fail_bosch_brake_non_bosch_steering():
    message = check_produced_car(_selection(SEDAN, GM, BOSCH_B, MOBIS))
    assert "FAIL" in message
