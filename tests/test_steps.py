import pytest

from car_assembly.parts import CarType, EngineType, BrakeType, SteeringType
from car_assembly.selection import CarSelection
from car_assembly.steps import build_first_step, PartSelectionStep, RunTestStep


@pytest.fixture
def chain():
    """One shared wizard chain per test - steps are stateless except for
    their fixed next/previous wiring, so this is safe to reuse within a test."""
    car_type_step = build_first_step()
    engine_step = car_type_step.next_step
    brake_step = engine_step.next_step
    steering_step = brake_step.next_step
    run_test_step = steering_step.next_step
    return car_type_step, engine_step, brake_step, steering_step, run_test_step


# ---------------------------------------------------------------------------
# chain wiring
# ---------------------------------------------------------------------------

def test_chain_has_expected_step_types(chain):
    car_type_step, engine_step, brake_step, steering_step, run_test_step = chain
    for step in (car_type_step, engine_step, brake_step, steering_step):
        assert isinstance(step, PartSelectionStep)
    assert isinstance(run_test_step, RunTestStep)


def test_first_step_cannot_go_back(chain):
    car_type_step, *_ = chain
    assert car_type_step.previous() is None


def test_each_selection_step_goes_back_to_the_previous_one(chain):
    car_type_step, engine_step, brake_step, steering_step, _ = chain
    assert engine_step.previous() is car_type_step
    assert brake_step.previous() is engine_step
    assert steering_step.previous() is brake_step


def test_run_test_step_back_goes_to_car_type_step_not_steering(chain):
    car_type_step, _, _, steering_step, run_test_step = chain
    assert run_test_step.previous() is car_type_step
    assert run_test_step.previous() is not steering_step


# ---------------------------------------------------------------------------
# validate() range checks (ported from the old validate_range tests)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ans", [1, 2, 3])
def test_car_type_step_accepts_1_to_3(chain, ans):
    car_type_step, *_ = chain
    assert car_type_step.validate(ans) is None


@pytest.mark.parametrize("ans", [0, 4, -1])
def test_car_type_step_rejects_outside_1_to_3(chain, ans):
    car_type_step, *_ = chain
    assert car_type_step.validate(ans) is not None


@pytest.mark.parametrize("ans", [0, 1, 2, 3, 4])
def test_engine_step_accepts_0_to_4(chain, ans):
    _, engine_step, *_ = chain
    assert engine_step.validate(ans) is None


@pytest.mark.parametrize("ans", [-1, 5])
def test_engine_step_rejects_outside_0_to_4(chain, ans):
    _, engine_step, *_ = chain
    assert engine_step.validate(ans) is not None


@pytest.mark.parametrize("ans", [0, 1, 2, 3])
def test_brake_step_accepts_0_to_3(chain, ans):
    _, _, brake_step, _, _ = chain
    assert brake_step.validate(ans) is None


@pytest.mark.parametrize("ans", [-1, 4])
def test_brake_step_rejects_outside_0_to_3(chain, ans):
    _, _, brake_step, _, _ = chain
    assert brake_step.validate(ans) is not None


@pytest.mark.parametrize("ans", [0, 1, 2])
def test_steering_step_accepts_0_to_2(chain, ans):
    _, _, _, steering_step, _ = chain
    assert steering_step.validate(ans) is None


@pytest.mark.parametrize("ans", [-1, 3])
def test_steering_step_rejects_outside_0_to_2(chain, ans):
    _, _, _, steering_step, _ = chain
    assert steering_step.validate(ans) is not None


@pytest.mark.parametrize("ans", [0, 1, 2])
def test_run_test_step_accepts_0_to_2(chain, ans):
    *_, run_test_step = chain
    assert run_test_step.validate(ans) is None


@pytest.mark.parametrize("ans", [-1, 3])
def test_run_test_step_rejects_outside_0_to_2(chain, ans):
    *_, run_test_step = chain
    assert run_test_step.validate(ans) is not None


# ---------------------------------------------------------------------------
# render(): menu text includes the step-specific prompt
# ---------------------------------------------------------------------------

def test_car_type_step_render_lists_car_types(chain):
    car_type_step, *_ = chain
    text = car_type_step.render()
    assert "1. Sedan" in text
    assert "2. SUV" in text
    assert "3. Truck" in text


def test_run_test_step_render_lists_run_and_test(chain):
    *_, run_test_step = chain
    text = run_test_step.render()
    assert "1. RUN" in text
    assert "2. Test" in text


# ---------------------------------------------------------------------------
# apply(): mutates CarSelection, returns (actions, next_step)
# ---------------------------------------------------------------------------

def test_car_type_step_apply_sets_selection_and_advances(chain):
    car_type_step, engine_step, *_ = chain
    selection = CarSelection()
    actions, next_step = car_type_step.apply(selection, 1)
    assert selection.car_type == CarType.SEDAN
    assert len(actions) == 1
    message, delay_ms = actions[0]
    assert "Sedan" in message
    assert delay_ms == 800
    assert next_step is engine_step


def test_run_test_step_apply_run_returns_single_action_and_loops_on_self(chain):
    *_, run_test_step = chain
    selection = CarSelection(
        car_type=CarType.SEDAN, engine=EngineType.GM,
        brake=BrakeType.MANDO, steering=SteeringType.BOSCH,
    )
    actions, next_step = run_test_step.apply(selection, 1)
    assert len(actions) == 1
    assert "자동차가 동작됩니다." in actions[0][0]
    assert actions[0][1] == 2000
    assert next_step is run_test_step


def test_run_test_step_apply_test_returns_two_actions(chain):
    *_, run_test_step = chain
    selection = CarSelection(
        car_type=CarType.SEDAN, engine=EngineType.GM,
        brake=BrakeType.CONTINENTAL, steering=SteeringType.BOSCH,
    )
    actions, next_step = run_test_step.apply(selection, 2)
    assert [msg for msg, _ in actions] == [
        "Test...",
        "FAIL\nSedan에는 Continental제동장치 사용 불가",
    ]
    assert [ms for _, ms in actions] == [1500, 2000]
    assert next_step is run_test_step
