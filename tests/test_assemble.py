import pytest

import assemble
from parts import CarType, EngineType, BrakeType, SteeringType
from assemble import (
    is_valid_range,
    select_car_type,
    select_engine,
    select_brake,
    select_steering,
    is_valid_check,
    run_produced_car,
    test_produced_car,
)

SEDAN, SUV, TRUCK = CarType.SEDAN, CarType.SUV, CarType.TRUCK
GM, TOYOTA, WIA = EngineType.GM, EngineType.TOYOTA, EngineType.WIA
MANDO, CONTINENTAL, BOSCH_B = BrakeType.MANDO, BrakeType.CONTINENTAL, BrakeType.BOSCH
BOSCH_S, MOBIS = SteeringType.BOSCH, SteeringType.MOBIS


# ---------------------------------------------------------------------------
# is_valid_range
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ans", [1, 2, 3])
def test_valid_range_step0_accepts_1_to_3(ans):
    assert is_valid_range(0, ans) is True


@pytest.mark.parametrize("ans", [0, 4, -1])
def test_valid_range_step0_rejects_outside_1_to_3(ans):
    assert is_valid_range(0, ans) is False


@pytest.mark.parametrize("ans", [0, 1, 2, 3, 4])
def test_valid_range_step1_accepts_0_to_4(ans):
    assert is_valid_range(1, ans) is True


@pytest.mark.parametrize("ans", [-1, 5])
def test_valid_range_step1_rejects_outside_0_to_4(ans):
    assert is_valid_range(1, ans) is False


@pytest.mark.parametrize("ans", [0, 1, 2, 3])
def test_valid_range_step2_accepts_0_to_3(ans):
    assert is_valid_range(2, ans) is True


@pytest.mark.parametrize("ans", [-1, 4])
def test_valid_range_step2_rejects_outside_0_to_3(ans):
    assert is_valid_range(2, ans) is False


@pytest.mark.parametrize("ans", [0, 1, 2])
def test_valid_range_step3_accepts_0_to_2(ans):
    assert is_valid_range(3, ans) is True


@pytest.mark.parametrize("ans", [-1, 3])
def test_valid_range_step3_rejects_outside_0_to_2(ans):
    assert is_valid_range(3, ans) is False


@pytest.mark.parametrize("ans", [0, 1, 2])
def test_valid_range_step4_accepts_0_to_2(ans):
    assert is_valid_range(4, ans) is True


@pytest.mark.parametrize("ans", [-1, 3])
def test_valid_range_step4_rejects_outside_0_to_2(ans):
    assert is_valid_range(4, ans) is False


# ---------------------------------------------------------------------------
# selection functions: they set module globals and print a confirmation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ans, expected_snippet",
    [(1, "Sedan"), (2, "SUV"), (3, "Truck")],
)
def test_select_car_type_sets_global_and_prints(capsys, ans, expected_snippet):
    select_car_type(ans)
    assert assemble.q0 == CarType(ans)
    assert expected_snippet in capsys.readouterr().out


@pytest.mark.parametrize(
    "ans, expected_snippet",
    [(1, "GM"), (2, "TOYOTA"), (3, "WIA"), (4, "고장난 엔진")],
)
def test_select_engine_sets_global_and_prints(capsys, ans, expected_snippet):
    select_engine(ans)
    assert assemble.q1 == EngineType(ans)
    assert expected_snippet in capsys.readouterr().out


@pytest.mark.parametrize(
    "ans, expected_snippet",
    [(1, "MANDO"), (2, "CONTINENTAL"), (3, "BOSCH")],
)
def test_select_brake_sets_global_and_prints(capsys, ans, expected_snippet):
    select_brake(ans)
    assert assemble.q2 == BrakeType(ans)
    assert expected_snippet in capsys.readouterr().out


@pytest.mark.parametrize(
    "ans, expected_snippet",
    [(1, "BOSCH"), (2, "MOBIS")],
)
def test_select_steering_sets_global_and_prints(capsys, ans, expected_snippet):
    select_steering(ans)
    assert assemble.q3 == SteeringType(ans)
    assert expected_snippet in capsys.readouterr().out


# ---------------------------------------------------------------------------
# is_valid_check: compatibility rules between parts
# ---------------------------------------------------------------------------

def _set_selection(car_type, engine, brake, steering):
    assemble.q0 = car_type
    assemble.q1 = engine
    assemble.q2 = brake
    assemble.q3 = steering


def test_is_valid_check_true_for_fully_compatible_combo():
    _set_selection(SEDAN, GM, MANDO, BOSCH_S)
    assert is_valid_check() is True


def test_is_valid_check_false_sedan_with_continental_brake():
    _set_selection(SEDAN, GM, CONTINENTAL, BOSCH_S)
    assert is_valid_check() is False


def test_is_valid_check_false_suv_with_toyota_engine():
    _set_selection(SUV, TOYOTA, MANDO, BOSCH_S)
    assert is_valid_check() is False


def test_is_valid_check_false_truck_with_wia_engine():
    _set_selection(TRUCK, WIA, CONTINENTAL, BOSCH_S)
    assert is_valid_check() is False


def test_is_valid_check_false_truck_with_mando_brake():
    _set_selection(TRUCK, GM, MANDO, BOSCH_S)
    assert is_valid_check() is False


def test_is_valid_check_false_bosch_brake_with_non_bosch_steering():
    _set_selection(SEDAN, GM, BOSCH_B, MOBIS)
    assert is_valid_check() is False


def test_is_valid_check_true_bosch_brake_with_bosch_steering():
    _set_selection(SEDAN, GM, BOSCH_B, BOSCH_S)
    assert is_valid_check() is True


# ---------------------------------------------------------------------------
# run_produced_car
# ---------------------------------------------------------------------------

def test_run_produced_car_incompatible_parts_does_not_run(capsys):
    _set_selection(SEDAN, GM, CONTINENTAL, BOSCH_S)
    run_produced_car()
    out = capsys.readouterr().out
    assert "자동차가 동작되지 않습니다" in out
    assert "자동차가 동작됩니다" not in out


def test_run_produced_car_broken_engine_does_not_move(capsys):
    _set_selection(SEDAN, EngineType.BROKEN, MANDO, BOSCH_S)
    run_produced_car()
    out = capsys.readouterr().out
    assert "엔진이 고장나있습니다" in out
    assert "자동차가 움직이지 않습니다" in out


def test_run_produced_car_valid_combo_prints_full_spec(capsys):
    _set_selection(SEDAN, GM, MANDO, BOSCH_S)
    run_produced_car()
    out = capsys.readouterr().out
    assert "Car Type : Sedan" in out
    assert "Engine   : GM" in out
    assert "Brake    : Mando" in out
    assert "Steering : Bosch" in out
    assert "자동차가 동작됩니다" in out


# ---------------------------------------------------------------------------
# test_produced_car
# ---------------------------------------------------------------------------

def test_produced_car_pass_for_compatible_combo(capsys):
    _set_selection(SEDAN, GM, MANDO, BOSCH_S)
    test_produced_car()
    assert "PASS" in capsys.readouterr().out


def test_produced_car_fail_sedan_continental(capsys):
    _set_selection(SEDAN, GM, CONTINENTAL, BOSCH_S)
    test_produced_car()
    assert "FAIL" in capsys.readouterr().out


def test_produced_car_fail_suv_toyota(capsys):
    _set_selection(SUV, TOYOTA, MANDO, BOSCH_S)
    test_produced_car()
    assert "FAIL" in capsys.readouterr().out


def test_produced_car_fail_truck_wia(capsys):
    _set_selection(TRUCK, WIA, CONTINENTAL, BOSCH_S)
    test_produced_car()
    assert "FAIL" in capsys.readouterr().out


def test_produced_car_fail_truck_mando(capsys):
    _set_selection(TRUCK, GM, MANDO, BOSCH_S)
    test_produced_car()
    assert "FAIL" in capsys.readouterr().out


def test_produced_car_fail_bosch_brake_non_bosch_steering(capsys):
    _set_selection(SEDAN, GM, BOSCH_B, MOBIS)
    test_produced_car()
    assert "FAIL" in capsys.readouterr().out
