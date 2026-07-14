from typing import List, Optional, Protocol, Tuple

from .selection import CarSelection
from .actions import select_car_type, select_engine, select_brake, select_steering
from .actions import run_produced_car, test_produced_car

Action = Tuple[str, int]  # (message, delay_ms)


class Step(Protocol):
    """One screen of the wizard. main()'s loop only talks to this
    interface, so adding a new step never requires touching main()."""

    def render(self) -> str:
        ...

    def validate(self, ans: int) -> Optional[str]:
        """Return an error message if ans is out of range for this step."""
        ...

    def previous(self) -> Optional["Step"]:
        """Step to go back to on ans == 0, or None if this step can't go back."""
        ...

    def apply(self, selection: CarSelection, ans: int) -> Tuple[List[Action], "Step"]:
        """Mutate/use selection for ans, returning (messages to render, next step)."""
        ...


class PartSelectionStep:
    """A step that lets the user pick one part and stores it on
    CarSelection. CarType/Engine/Brake/Steering steps only differ in
    their menu text, accepted range and which setter they call."""

    def __init__(self, menu_lines, min_ans, max_ans, range_error, select_fn):
        self._menu_lines = menu_lines
        self._min_ans = min_ans
        self._max_ans = max_ans
        self._range_error = range_error
        self._select_fn = select_fn
        self.previous_step: Optional[Step] = None
        self.next_step: Optional[Step] = None

    def render(self) -> str:
        return "\n".join(self._menu_lines + ["==============================="])

    def validate(self, ans: int) -> Optional[str]:
        if ans < self._min_ans or ans > self._max_ans:
            return self._range_error
        return None

    def previous(self) -> Optional[Step]:
        return self.previous_step

    def apply(self, selection: CarSelection, ans: int) -> Tuple[List[Action], Step]:
        message = self._select_fn(selection, ans)
        return [(message, 800)], self.next_step


class RunTestStep:
    """Final step: RUN builds/drives the car, Test reports PASS/FAIL.
    Unlike the selection steps it doesn't advance - it loops on itself."""

    _MENU_LINES = [
        "멋진 차량이 완성되었습니다.",
        "0. 처음 화면으로 돌아가기",
        "1. RUN",
        "2. Test",
    ]
    _RANGE_ERROR = "ERROR :: Run 또는 Test 중 하나를 선택 필요"

    def __init__(self):
        self.previous_step: Optional[Step] = None

    def render(self) -> str:
        return "\n".join(self._MENU_LINES + ["==============================="])

    def validate(self, ans: int) -> Optional[str]:
        if ans < 0 or ans > 2:
            return self._RANGE_ERROR
        return None

    def previous(self) -> Optional[Step]:
        return self.previous_step

    def apply(self, selection: CarSelection, ans: int) -> Tuple[List[Action], Step]:
        if ans == 1:
            return [(run_produced_car(selection), 2000)], self
        return [("Test...", 1500), (test_produced_car(selection), 2000)], self


_CAR_TYPE_MENU = [
    "        ______________",
    "       /|            |",
    "  ____/_|_____________|____",
    " |                      O  |",
    " '-(@)----------------(@)--'",
    "===============================",
    "어떤 차량 타입을 선택할까요?",
    "1. Sedan",
    "2. SUV",
    "3. Truck",
]

_ENGINE_MENU = [
    "어떤 엔진을 탑재할까요?",
    "0. 뒤로가기",
    "1. GM",
    "2. TOYOTA",
    "3. WIA",
    "4. 고장난 엔진",
]

_BRAKE_MENU = [
    "어떤 제동장치를 선택할까요?",
    "0. 뒤로가기",
    "1. MANDO",
    "2. CONTINENTAL",
    "3. BOSCH",
]

_STEERING_MENU = [
    "어떤 조향장치를 선택할까요?",
    "0. 뒤로가기",
    "1. BOSCH",
    "2. MOBIS",
]


def build_first_step() -> Step:
    """Wire up the fixed wizard chain: car type -> engine -> brake ->
    steering -> run/test. Returns the entry point (car type step)."""
    car_type_step = PartSelectionStep(
        _CAR_TYPE_MENU, 1, 3,
        "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능",
        select_car_type,
    )
    engine_step = PartSelectionStep(
        _ENGINE_MENU, 0, 4,
        "ERROR :: 엔진은 1 ~ 4 범위만 선택 가능",
        select_engine,
    )
    brake_step = PartSelectionStep(
        _BRAKE_MENU, 0, 3,
        "ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능",
        select_brake,
    )
    steering_step = PartSelectionStep(
        _STEERING_MENU, 0, 2,
        "ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능",
        select_steering,
    )
    run_test_step = RunTestStep()

    car_type_step.next_step = engine_step
    engine_step.next_step = brake_step
    brake_step.next_step = steering_step
    steering_step.next_step = run_test_step

    engine_step.previous_step = car_type_step
    brake_step.previous_step = engine_step
    steering_step.previous_step = brake_step
    run_test_step.previous_step = car_type_step  # "back to start", not to steering

    return car_type_step
