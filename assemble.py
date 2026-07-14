import sys
import time

from parts import CarType, EngineType, BrakeType, SteeringType

CLEAR_SCREEN = "\033[H\033[2J"

CarType_Q = 0
Engine_Q = 1
brakeSystem_Q = 2
SteeringSystem_Q = 3
Run_Test = 4

q0 = 0
q1 = 0
q2 = 0
q3 = 0
q4 = 0


def delay(ms):
    t = ms / 1000.0
    time.sleep(t)


def clear():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def show_menu(step):
    clear()
    if step == 0:
        print("        ______________")
        print("       /|            |")
        print("  ____/_|_____________|____")
        print(" |                      O  |")
        print(" '-(@)----------------(@)--'")
        print("===============================")
        print("어떤 차량 타입을 선택할까요?")
        print("1. Sedan")
        print("2. SUV")
        print("3. Truck")
    elif step == 1:
        print("어떤 엔진을 탑재할까요?")
        print("0. 뒤로가기")
        print("1. GM")
        print("2. TOYOTA")
        print("3. WIA")
        print("4. 고장난 엔진")
    elif step == 2:
        print("어떤 제동장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. MANDO")
        print("2. CONTINENTAL")
        print("3. BOSCH")
    elif step == 3:
        print("어떤 조향장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. BOSCH")
        print("2. MOBIS")
    elif step == 4:
        print("멋진 차량이 완성되었습니다.")
        print("0. 처음 화면으로 돌아가기")
        print("1. RUN")
        print("2. Test")
    print("===============================")


def is_valid_range(step, ans):
    if step == 0:
        if ans < 1 or ans > 3:
            print("ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능")
            return False
    if step == 1:
        if ans < 0 or ans > 4:
            print("ERROR :: 엔진은 1 ~ 4 범위만 선택 가능")
            return False
    if step == 2:
        if ans < 0 or ans > 3:
            print("ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능")
            return False
    if step == 3:
        if ans < 0 or ans > 2:
            print("ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능")
            return False
    if step == 4:
        if ans < 0 or ans > 2:
            print("ERROR :: Run 또는 Test 중 하나를 선택 필요")
            return False
    return True


def select_car_type(a):
    global q0
    q0 = CarType(a)
    print(f"차량 타입으로 {q0.label}을 선택하셨습니다.")


def select_engine(a):
    global q1
    q1 = EngineType(a)
    if q1 == EngineType.BROKEN:
        print("고장난 엔진을 선택하셨습니다.")
    else:
        print(f"{q1.label} 엔진을 선택하셨습니다.")


def select_brake(a):
    global q2
    q2 = BrakeType(a)
    print(f"{q2.name} 제동장치를 선택하셨습니다.")


def select_steering(a):
    global q3
    q3 = SteeringType(a)
    print(f"{q3.name} 조향장치를 선택하셨습니다.")


def is_valid_check():
    if q0 == CarType.SEDAN and q2 == BrakeType.CONTINENTAL:
        return False
    if q0 == CarType.SUV and q1 == EngineType.TOYOTA:
        return False
    if q0 == CarType.TRUCK and q1 == EngineType.WIA:
        return False
    if q0 == CarType.TRUCK and q2 == BrakeType.MANDO:
        return False
    if q2 == BrakeType.BOSCH and q3 != SteeringType.BOSCH:
        return False
    return True


def run_produced_car():
    if not is_valid_check():
        print("자동차가 동작되지 않습니다")
        return
    if q1 == EngineType.BROKEN:
        print("엔진이 고장나있습니다.")
        print("자동차가 움직이지 않습니다.")
        return

    print(f"Car Type : {q0.label}")
    print(f"Engine   : {q1.label}")
    print(f"Brake    : {q2.label}")
    print(f"Steering : {q3.label}")

    print("자동차가 동작됩니다.")


def test_produced_car():
    if q0 == CarType.SEDAN and q2 == BrakeType.CONTINENTAL:
        print("FAIL\nSedan에는 Continental제동장치 사용 불가")
    elif q0 == CarType.SUV and q1 == EngineType.TOYOTA:
        print("FAIL\nSUV에는 TOYOTA엔진 사용 불가")
    elif q0 == CarType.TRUCK and q1 == EngineType.WIA:
        print("FAIL\nTruck에는 WIA엔진 사용 불가")
    elif q0 == CarType.TRUCK and q2 == BrakeType.MANDO:
        print("FAIL\nTruck에는 Mando제동장치 사용 불가")
    elif q2 == BrakeType.BOSCH and q3 != SteeringType.BOSCH:
        print("FAIL\nBosch제동장치에는 Bosch조향장치 이외 사용 불가")
    else:
        print("PASS")


def main():
    step = 0
    while True:
        show_menu(step)
        buf = input("INPUT > ").strip()

        if buf == "exit":
            print("바이바이")
            break

        try:
            ans = int(buf)
        except:
            print("ERROR :: 숫자만 입력 가능")
            delay(800)
            continue

        if not is_valid_range(step, ans):
            delay(800)
            continue

        if ans == 0:
            if step == 4:
                step = 0
            elif step > 0:
                step = step - 1
            continue

        if step == 0:
            select_car_type(ans)
            delay(800)
            step = 1
        elif step == 1:
            select_engine(ans)
            delay(800)
            step = 2
        elif step == 2:
            select_brake(ans)
            delay(800)
            step = 3
        elif step == 3:
            select_steering(ans)
            delay(800)
            step = 4
        elif step == 4:
            if ans == 1:
                run_produced_car()
                delay(2000)
            elif ans == 2:
                print("Test...")
                delay(1500)
                test_produced_car()
                delay(2000)


if __name__ == "__main__":
    main()
