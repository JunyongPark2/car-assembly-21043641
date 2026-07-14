from parts import EngineType
from rules import find_violations


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
