from car_assembly.app import CarAssemblyApp
from conftest import FakeInput, FakeRenderer


def _run(answers):
    renderer = FakeRenderer()
    CarAssemblyApp(
        renderer=renderer,
        input_provider=FakeInput(answers),
        delay_fn=lambda ms: None,
    ).run()
    return renderer


def test_full_happy_path_runs_compatible_car():
    renderer = _run(["1", "1", "1", "1", "1", "exit"])
    joined = "\n".join(renderer.frames)
    assert "차량 타입으로 Sedan을 선택하셨습니다." in joined
    assert "GM 엔진을 선택하셨습니다." in joined
    assert "MANDO 제동장치를 선택하셨습니다." in joined
    assert "BOSCH 조향장치를 선택하셨습니다." in joined
    assert "자동차가 동작됩니다." in joined
    assert "바이바이" in joined


def test_full_path_tests_incompatible_car():
    # Sedan + Continental brake violates a compatibility rule.
    renderer = _run(["1", "1", "2", "1", "2", "exit"])
    joined = "\n".join(renderer.frames)
    assert "Test..." in joined
    assert "FAIL" in joined
    assert "Sedan에는 Continental제동장치 사용 불가" in joined


def test_invalid_numeric_input_shows_error_and_reprompts():
    renderer = _run(["9", "1", "1", "1", "1", "exit"])
    joined = "\n".join(renderer.frames)
    assert "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능" in joined


def test_non_numeric_input_shows_error_and_reprompts():
    renderer = _run(["abc", "1", "1", "1", "1", "exit"])
    joined = "\n".join(renderer.frames)
    assert "ERROR :: 숫자만 입력 가능" in joined


def test_back_navigation_returns_to_previous_step():
    # Go to engine step, then back to car-type step, then proceed fully.
    renderer = _run(["1", "0", "2", "1", "1", "1", "exit"])
    joined = "\n".join(renderer.frames)
    assert "차량 타입으로 SUV을 선택하셨습니다." in joined


def test_run_test_step_back_resets_to_car_type_step():
    # From the final step, "back" goes all the way to step 0, not to steering.
    renderer = _run(["1", "1", "1", "1", "0", "2", "1", "1", "1", "exit"])
    joined = "\n".join(renderer.frames)
    assert joined.count("차량 타입으로 SUV을 선택하셨습니다.") == 1


def test_broken_engine_prevents_car_from_moving():
    renderer = _run(["1", "4", "1", "1", "1", "exit"])
    joined = "\n".join(renderer.frames)
    assert "엔진이 고장나있습니다." in joined
    assert "자동차가 움직이지 않습니다." in joined


def test_clear_is_called_before_every_menu_render():
    renderer = _run(["1", "1", "1", "1", "exit"])
    assert renderer.clear_count >= 5
