# assemble.py 코드 분석

## 개요
대화형 CLI로 차량(Sedan/SUV/Truck)에 엔진/제동장치/조향장치를 조합해
"조립"하고, 조합의 호환성을 RUN 또는 TEST로 확인하는 단일 파일(`assemble.py`, 275줄)
스크립트. 클래스 없이 함수 + 모듈 전역 변수로만 구성되어 있음.

## 데이터 모델 (현재)
- 부품 종류는 정수 상수로 정의됨: `SEDAN/SUV/TRUCK`, `GM/TOYOTA/WIA`,
  `MANDO/CONTINENTAL/BOSCH_B`, `BOSCH_S/MOBIS`.
- 사용자의 현재 선택 상태는 모듈 전역 변수 `q0, q1, q2, q3` (+ 미사용 `q4`)에
  저장됨. 함수 간 데이터 전달 대신 전역 상태를 직접 read/write.
- 부품 이름(한글/영문 표시 문자열)은 여러 곳에 하드코딩된 if/elif 체인으로
  중복 정의됨 (`show_menu`, `select_*`, `run_produced_car`, `test_produced_car`
  4곳에서 유사한 매핑이 반복).

## 함수별 역할

| 함수 | 역할 | 비고 |
|---|---|---|
| `delay(ms)` | sleep 래퍼 | |
| `clear()` | 화면 지우기 (ANSI escape) | I/O |
| `show_menu(step)` | step에 따라 프롬프트 출력 | I/O + 분기 |
| `is_valid_range(step, ans)` | step별 입력값 유효 범위 검사 | 검증 로직, step에 종속적 |
| `select_car_type/engine/brake/steering(a)` | 전역 변수 갱신 + 확인 메시지 출력 | 상태 변경과 I/O가 결합됨 |
| `is_valid_check()` | 부품 조합 호환성 규칙 5개를 하드코딩 체크 | `test_produced_car`와 로직 중복 |
| `run_produced_car()` | 호환성 검사 후 조립 결과 출력 | `is_valid_check` 재사용하지만 고장 엔진 처리는 별도 |
| `test_produced_car()` | 호환성 규칙을 다시 하나씩 검사해 PASS/FAIL 사유 출력 | `is_valid_check()`와 규칙이 **두 번** 구현됨 |
| `main()` | 입력 루프, step 전이, 전역 상태 기반 분기 | 모든 관심사가 한 곳에 응집 |

## 주요 문제점 (리팩토링 동기)

1. **전역 가변 상태 (God state)**: `q0~q3`가 모듈 전역이라 함수들이 서로
   암묵적으로 결합됨. 테스트 시 매번 수동으로 리셋해야 했음
   (`tests/conftest.py`의 `reset_globals` 참고).
2. **SRP 위반**: 거의 모든 함수가 "상태 변경 + 콘솔 출력"을 동시에 수행.
   입력(stdin)과 출력(stdout)이 로직과 강하게 결합되어 있어 로직만 따로
   테스트하거나 재사용(예: GUI, API로 노출)할 수 없음.
3. **OCP 위반**: 새로운 차량 타입/부품/호환성 규칙을 추가하려면
   `show_menu`, `is_valid_range`, `select_*`, `is_valid_check`,
   `test_produced_car`, `main`의 if/elif 체인을 전부 손대야 함.
4. **로직 중복**: 호환성 규칙이 `is_valid_check()`와 `test_produced_car()`에
   **각각 다른 자료구조(bool vs 메시지 문자열)로 두 번** 구현되어 있음.
   규칙을 하나 고치면 다른 한 곳도 반드시 같이 고쳐야 하는데, 이를
   강제하는 장치가 없음 (버그 유발 지점).
5. **매직 넘버/문자열 산재**: 부품 이름 문자열이 여러 함수에 중복 하드코딩.
6. **DIP 위반**: `input()`/`print()`/`time.sleep()`을 로직 함수들이 직접
   호출하여, 콘솔이 아닌 환경(테스트, 다른 UI)에서 재사용 불가.
7. **`main()`의 낮은 응집도**: 입력 파싱, 범위 검증, step 전이, 화면 전환
   딜레이까지 하나의 while 루프에 모두 들어있어 각 관심사를 독립적으로
   테스트/변경하기 어려움.

## 현재 테스트 커버리지
`tests/test_assemble.py` (58 tests) — 리팩토링 전 안전망으로 작성됨.
`is_valid_range`, `select_*`, `is_valid_check`, `run_produced_car`,
`test_produced_car`의 **현재 동작(관찰 가능한 출력)** 을 고정.
`main()`의 입력 루프 자체는 아직 테스트되지 않음 (I/O 결합으로 인해 테스트
어려움 → 리팩토링 대상).
