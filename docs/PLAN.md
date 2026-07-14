# 리팩토링 계획

목표: `assemble.py`의 동작(관찰 가능한 CLI 출력)을 유지하면서 SOLID 원칙을
따르는 구조로 단계적으로 재구성한다. 각 Phase는 독립적으로 커밋 가능해야
하며, 완료 시점마다 `tests/test_assemble.py` 및 새로 추가한 테스트가 모두
통과해야 다음 Phase로 넘어간다.

전제: `ANALYSIS.md`에서 정리한 문제점 — 전역 상태, SRP/OCP 위반, 규칙 로직
중복, DIP 위반 — 을 순서대로 제거한다. 뒤 Phase일수록 앞 Phase가 만든
추상화에 의존하므로 순서를 바꾸지 않는다.

---

## Phase 0 — 안전망 (완료)
- `tests/test_assemble.py`, `tests/conftest.py` 작성 완료.
- 이후 모든 Phase는 "리팩토링 전/후 관찰 가능한 출력이 동일함"을 이 테스트
  스위트(및 각 Phase에서 추가하는 테스트)로 검증한다.

## Phase 1 — 부품 정의를 데이터로 통합 (OCP, DRY)
**문제**: 부품 이름 문자열/ID가 `show_menu`, `select_*`, `run_produced_car`,
`test_produced_car`에 각각 하드코딩되어 4곳에서 중복.

**작업**:
- `parts.py` 신설. `CarType`, `EngineType`, `BrakeType`, `SteeringType`을
  `Enum`으로 정의하고, 각 멤버에 표시 이름(한글 라벨)을 매핑하는 단일
  딕셔너리(또는 `Enum` + `@property`)를 둔다.
- 기존 `SEDAN/SUV/TRUCK` 등 정수 상수는 이 Enum으로 대체.
- "고장난 엔진"처럼 정상 부품이 아닌 특수 케이스도 Enum 멤버로 명시.

**SOLID 효과**: 새 부품 하나 추가 = Enum에 멤버 하나 추가로 끝 (OCP).
이름 문자열의 단일 진실 공급원(SSOT) 확보.

**완료 기준**: 기존 58개 테스트를 새 심볼(Enum)을 참조하도록 최소 수정 후
통과. 출력 문자열은 1바이트도 바뀌지 않아야 함.

---

## Phase 2 — 전역 상태 제거 → `CarSelection` 값 객체 (SRP)
**문제**: `q0~q3` 모듈 전역이 여러 함수에 암묵적으로 공유됨.

**작업**:
- `CarSelection` (dataclass): `car_type`, `engine`, `brake`, `steering`
  필드(Optional, 초기값 None)를 갖는 상태 컨테이너.
- `select_car_type/engine/brake/steering`을 `CarSelection`의 메서드 또는
  순수 함수(`selection.with_engine(x)` 등 불변 방식도 검토)로 전환하고,
  **콘솔 출력은 이 단계에서 함께 제거하지 않음** (Phase 4에서 처리) —
  단, 전역 변수 대신 인자로 받은 `CarSelection` 인스턴스를 변경/반환하도록만
  바꾼다. 한 번에 여러 관심사를 바꾸지 않기 위해 SRP 분리는 Phase 4로
  미룬다.
- `main()`은 이제 `CarSelection` 인스턴스 하나를 만들어 들고 다님.

**SOLID 효과**: 전역 상태 제거로 함수가 순수해지고 병렬 실행/재사용/테스트가
쉬워짐 (SRP: 상태 소유권이 명확한 객체로 이동).

**완료 기준**: 전역 `q0~q4` 완전 삭제. 테스트에서 `assemble.q0 = ...`처럼
전역을 직접 건드리던 부분을 `CarSelection` 생성으로 교체.

---

## Phase 3 — 호환성 규칙을 전략 패턴으로 추출 (OCP, DRY, 최우선 버그 제거)
**문제**: 동일한 5개 호환성 규칙이 `is_valid_check()`(bool)와
`test_produced_car()`(메시지 문자열)에 **두 번** 구현되어 있어 항상 같이
수정해야 하는데 강제되지 않음.

**작업**:
- `rules.py` 신설. `CompatibilityRule` 인터페이스(또는 `Protocol`):
  `check(selection: CarSelection) -> Optional[str]` — 위반 시 실패 사유
  문자열, 통과 시 `None`을 반환.
- 기존 5개 규칙(Sedan-Continental 불가, SUV-Toyota 불가, Truck-WIA 불가,
  Truck-Mando 불가, Bosch제동-비Bosch조향 불가)을 각각 별도 `Rule`
  객체/함수로 구현하고 리스트(`COMPATIBILITY_RULES`)로 관리.
- `is_valid_check()`와 `test_produced_car()`를 이 리스트를 순회하는
  **공용 헬퍼 하나**(`evaluate(selection) -> list[str]`, 위반 사유 목록 반환)
  기반으로 재구현. bool 필요하면 `not violations`, 메시지 필요하면
  `violations[0]` 등으로 파생.

**SOLID 효과**: 규칙 추가/변경 시 리스트에 항목 하나 추가/수정으로 끝
(OCP). 판정 로직과 메시지가 한 곳에만 존재 (DRY → 버그 원천 차단).

**완료 기준**: 기존 규칙 관련 테스트(호환성 케이스 전부) 그대로 통과 +
`rules.py`에 대한 단위 테스트 추가(규칙 개별 테스트).

---

## Phase 4 — I/O와 로직 분리 (SRP, DIP)
**문제**: 상태 변경 함수들이 `print()`를 직접 호출하고, `main()`이
`input()`/`time.sleep()`을 직접 호출해 로직이 콘솔에 강결합.

**작업**:
- `Renderer` 프로토콜(`show(text: str) -> None`, 메뉴 렌더 메서드 등)과
  `InputProvider` 프로토콜(`read() -> str`) 정의. 실제 구현은
  `ConsoleRenderer`/`ConsoleInput` (기존 `print`/`input`/`clear`/`delay` 이동).
- `select_car_type` 등에서 `print()` 제거 → 순수 로직(상태 변경)만 남기고,
  "선택되었습니다" 같은 확인 메시지는 호출부(애플리케이션 계층)가
  `Renderer`를 통해 출력하도록 이동.
- `run_produced_car`/`test_produced_car`도 문자열을 "반환"하도록 바꾸고,
  콘솔 출력은 이를 호출하는 애플리케이션 계층에서 `Renderer`로 수행.

**SOLID 효과**: 도메인 로직이 콘솔에 의존하지 않게 되어 DIP 충족,
"판단"과 "출력"의 책임 분리로 SRP 충족. 테스트에서 `capsys` 없이 순수
반환값만으로 검증 가능해짐 (테스트 단순화는 부수 효과).

**완료 기준**: 도메인 계층(`parts.py`, `rules.py`, `CarSelection`, 조립 판정
함수)에 `print`/`input` 의존이 전혀 없음을 grep으로 확인. 콘솔 출력
스냅샷은 Phase 0 테스트와 동일하게 유지(어댑터 계층 테스트로 이전).

---

## Phase 5 — 메뉴/스텝 내비게이션을 상태 머신으로 재구성 (OCP, LSP)
**문제**: `show_menu`, `is_valid_range`, `main`의 step 분기(`step==0..4`)가
3곳에 병렬로 존재 — 스텝 하나 추가하려면 3곳을 동시에 고쳐야 함.

**작업**:
- `Step` 인터페이스(`prompt() -> str`, `valid_range() -> range`,
  `apply(selection, ans) -> CarSelection`, `next_step() -> Step | None`)를
  정의하고, 기존 5단계(차종/엔진/제동/조향/실행-테스트)를 각각 구체
  클래스 또는 데이터로 표현.
- `main()`의 while 루프는 "현재 `Step` 객체"만 들고 다니며, 분기 없이
  `step.prompt()`, `step.valid_range()`, `step.apply(...)` 호출만 수행.
- 각 `Step` 구현체는 서로 치환 가능해야 함(LSP) — 특정 스텝만 예외적으로
  다른 인터페이스를 요구하지 않도록 주의.

**SOLID 효과**: 새 스텝(예: "타이어 선택") 추가 = 새 `Step` 클래스 하나
추가 + 체인에 연결, 기존 스텝/코드 수정 불필요 (OCP).

**완료 기준**: `main()`에 `if step == N` 형태의 분기가 더 이상 존재하지
않음. 스텝 전이(뒤로가기 포함) 동작이 기존과 동일함을 통합 테스트로 확인.

---

## Phase 6 — 애플리케이션 계층 조립 및 회귀 테스트 전면 정리
**작업**:
- `app.py`(또는 `main.py`)에서 `Renderer`, `InputProvider`, `Step` 체인,
  `CarSelection`을 조립하는 `CarAssemblyApp` 클래스 작성 (DIP: 구체
  구현은 생성 시점에 주입).
- `tests/`를 새 구조에 맞춰 재배치: `tests/test_parts.py`,
  `tests/test_rules.py`, `tests/test_selection.py`,
  `tests/test_app.py`(가짜 `InputProvider`/`Renderer`로 `main` 루프 전체를
  E2E로 테스트 — Phase 0에서는 불가능했던 부분).
- 기존 `assemble.py`는 새 모듈들을 조립해 실행하는 얇은 entrypoint로 축소.

**완료 기준**: 전체 테스트 스위트 통과, 수동 실행(`python assemble.py`)으로
기존과 동일한 CLI 동작(문구/순서) 확인.

## Phase 7 — 마무리 정리
- 죽은 코드/미사용 상수(`q4`, 미사용 import 등) 제거.
- 각 모듈에 대해 타입 힌트 점검, `ruff`/`mypy` 등 정적 검사(있다면) 통과.
- `ANALYSIS.md`를 리팩토링 후 구조에 맞게 갱신하거나, 새 `ARCHITECTURE.md`로
  대체 여부 결정.

---

## Phase별 SOLID 매핑 요약

| Phase | 주로 다루는 원칙 |
|---|---|
| 1 | OCP, DRY (SRP 사전 준비) |
| 2 | SRP (상태 소유권 분리) |
| 3 | OCP, DRY (가장 시급한 버그 원천 제거) |
| 4 | SRP, DIP (I/O와 로직 분리) |
| 5 | OCP, LSP (스텝 확장성) |
| 6 | DIP (조립부에서 구체 구현 주입), 통합 검증 |
| 7 | 정리 |

## 진행 방식
- Phase 하나 = 커밋 하나(또는 PR 하나) 단위로 진행.
- 각 Phase 종료 시 `pytest` 전체 통과 확인 후 다음 Phase 시작.
- Phase 3(규칙 중복 제거)이 실질적으로 가장 리스크가 높은 버그(규칙 불일치)를
  해결하므로, 일정상 우선순위를 조정해야 한다면 Phase 3을 앞당기는 것을
  고려할 수 있음(단, Phase 2의 `CarSelection`이 먼저 있어야 규칙 함수의
  시그니처가 깔끔해짐).
