from assemble import main


class FakeInput:
    """Feeds a scripted sequence of answers, standing in for stdin."""

    def __init__(self, answers):
        self._answers = list(answers)

    def read(self, prompt):
        return self._answers.pop(0)


class FakeRenderer:
    """Collects every rendered frame instead of writing to stdout."""

    def __init__(self):
        self.frames = []
        self.clear_count = 0

    def show(self, text=""):
        self.frames.append(text)

    def clear(self):
        self.clear_count += 1


def _run(answers):
    renderer = FakeRenderer()
    main(renderer=renderer, input_provider=FakeInput(answers), delay_fn=lambda ms: None)
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
