from parts import EngineType
from selection import CarSelection
from rules import find_violations
from io_adapters import ConsoleRenderer, ConsoleInput, delay


def build_menu(step):
    lines = []
    if step == 0:
        lines += [
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
    elif step == 1:
        lines += [
            "어떤 엔진을 탑재할까요?",
            "0. 뒤로가기",
            "1. GM",
            "2. TOYOTA",
            "3. WIA",
            "4. 고장난 엔진",
        ]
    elif step == 2:
        lines += [
            "어떤 제동장치를 선택할까요?",
            "0. 뒤로가기",
            "1. MANDO",
            "2. CONTINENTAL",
            "3. BOSCH",
        ]
    elif step == 3:
        lines += [
            "어떤 조향장치를 선택할까요?",
            "0. 뒤로가기",
            "1. BOSCH",
            "2. MOBIS",
        ]
    elif step == 4:
        lines += [
            "멋진 차량이 완성되었습니다.",
            "0. 처음 화면으로 돌아가기",
            "1. RUN",
            "2. Test",
        ]
    lines.append("===============================")
    return "\n".join(lines)


def validate_range(step, ans):
    """Return an error message if ans is out of range for step, else None."""
    if step == 0 and (ans < 1 or ans > 3):
        return "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능"
    if step == 1 and (ans < 0 or ans > 4):
        return "ERROR :: 엔진은 1 ~ 4 범위만 선택 가능"
    if step == 2 and (ans < 0 or ans > 3):
        return "ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능"
    if step == 3 and (ans < 0 or ans > 2):
        return "ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능"
    if step == 4 and (ans < 0 or ans > 2):
        return "ERROR :: Run 또는 Test 중 하나를 선택 필요"
    return None


def select_car_type(selection, a):
    car_type = selection.set_car_type(a)
    return f"차량 타입으로 {car_type.label}을 선택하셨습니다."


def select_engine(selection, a):
    engine = selection.set_engine(a)
    if engine == EngineType.BROKEN:
        return "고장난 엔진을 선택하셨습니다."
    return f"{engine.label} 엔진을 선택하셨습니다."


def select_brake(selection, a):
    brake = selection.set_brake(a)
    return f"{brake.name} 제동장치를 선택하셨습니다."


def select_steering(selection, a):
    steering = selection.set_steering(a)
    return f"{steering.name} 조향장치를 선택하셨습니다."


def is_valid_check(selection):
    return not find_violations(selection)


def run_produced_car(selection):
    if not is_valid_check(selection):
        return "자동차가 동작되지 않습니다"
    if selection.engine == EngineType.BROKEN:
        return "엔진이 고장나있습니다.\n자동차가 움직이지 않습니다."

    return "\n".join(
        [
            f"Car Type : {selection.car_type.label}",
            f"Engine   : {selection.engine.label}",
            f"Brake    : {selection.brake.label}",
            f"Steering : {selection.steering.label}",
            "자동차가 동작됩니다.",
        ]
    )


def test_produced_car(selection):
    violations = find_violations(selection)
    if violations:
        return f"FAIL\n{violations[0]}"
    return "PASS"


def main(renderer=None, input_provider=None, delay_fn=None):
    renderer = renderer or ConsoleRenderer()
    input_provider = input_provider or ConsoleInput()
    delay_fn = delay_fn or delay

    step = 0
    selection = CarSelection()
    while True:
        renderer.clear()
        renderer.show(build_menu(step))
        buf = input_provider.read("INPUT > ").strip()

        if buf == "exit":
            renderer.show("바이바이")
            break

        try:
            ans = int(buf)
        except ValueError:
            renderer.show("ERROR :: 숫자만 입력 가능")
            delay_fn(800)
            continue

        error = validate_range(step, ans)
        if error:
            renderer.show(error)
            delay_fn(800)
            continue

        if ans == 0:
            if step == 4:
                step = 0
            elif step > 0:
                step = step - 1
            continue

        if step == 0:
            renderer.show(select_car_type(selection, ans))
            delay_fn(800)
            step = 1
        elif step == 1:
            renderer.show(select_engine(selection, ans))
            delay_fn(800)
            step = 2
        elif step == 2:
            renderer.show(select_brake(selection, ans))
            delay_fn(800)
            step = 3
        elif step == 3:
            renderer.show(select_steering(selection, ans))
            delay_fn(800)
            step = 4
        elif step == 4:
            if ans == 1:
                renderer.show(run_produced_car(selection))
                delay_fn(2000)
            elif ans == 2:
                renderer.show("Test...")
                delay_fn(1500)
                renderer.show(test_produced_car(selection))
                delay_fn(2000)


if __name__ == "__main__":
    main()
