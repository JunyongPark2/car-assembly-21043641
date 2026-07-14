# 아키텍처 (리팩토링 후)

`PLAN.md`의 Phase 1~7을 거친 뒤의 최종 모듈 구조. 리팩토링 전 상태와 문제점은
`ANALYSIS.md`(역사적 기록)를 참고.

## 모듈 구성

| 모듈 | 책임 | 의존 |
|---|---|---|
| `parts.py` | `CarType/EngineType/BrakeType/SteeringType` Enum + 표시 라벨 | 없음 |
| `selection.py` | `CarSelection` — 사용자가 지금까지 고른 부품을 들고 다니는 값 객체 | `parts` |
| `rules.py` | `COMPATIBILITY_RULES` 전략 리스트 + `find_violations()` | `parts`, `selection` |
| `actions.py` | 순수 도메인 함수 (`select_*`, `is_valid_check`, `run_produced_car`, `test_produced_car`) — 문자열을 반환할 뿐 I/O 없음 | `parts`, `rules` |
| `steps.py` | `Step` 프로토콜(`render/validate/previous/apply`) + `PartSelectionStep`/`RunTestStep` + `build_first_step()` 체인 조립 | `selection`, `actions` |
| `io_adapters.py` | `Renderer`/`InputProvider` 프로토콜 + `ConsoleRenderer`/`ConsoleInput`/`delay` 구현체 | 없음 (표준 라이브러리만) |
| `app.py` | `CarAssemblyApp` — 합성근(composition root). Renderer/InputProvider/delay_fn과 Step 체인을 엮어 메인 루프 실행 | `selection`, `steps`, `io_adapters` |
| `assemble.py` | 실행 진입점. `CarAssemblyApp`을 생성해 실행하는 얇은 wrapper | `app` |

## 의존 방향

```
assemble.py -> app.py -> steps.py -> actions.py -> rules.py -> parts.py
                     \-> io_adapters.py         \-> selection.py
                     \-> selection.py
```

도메인 계층(`parts`, `selection`, `rules`, `actions`, `steps`)은 `io_adapters`에
의존하지 않는다 — `print`/`input`/`time.sleep` 호출이 전혀 없다. 콘솔에 대한
의존은 `app.py`(합성근)에서만 발생하며, `Renderer`/`InputProvider` 프로토콜을
통해 주입된다 (DIP).

## SOLID가 어디에 반영되었는지

- **SRP**: `selection.py`(상태 보유), `rules.py`(호환성 판정),
  `actions.py`(도메인 동작), `io_adapters.py`(콘솔 I/O), `app.py`(조립) —
  각 모듈이 변경되는 이유가 하나씩만 있음.
- **OCP**: 새 부품 = `parts.py`에 Enum 멤버 추가. 새 호환성 규칙 =
  `rules.py`의 `COMPATIBILITY_RULES`에 항목 추가. 새 마법사 단계 = `steps.py`에
  `Step` 구현체 추가 + `build_first_step()`에서 체인 연결. 기존 코드(특히
  `app.py`의 메인 루프)는 건드리지 않는다.
- **LSP**: `PartSelectionStep`과 `RunTestStep`은 서로 다른 동작(부품 선택 vs
  실행/테스트)을 하지만 동일한 `Step` 프로토콜(`render/validate/previous/apply`)로
  치환 가능 — `app.py`는 구체 타입을 구분하지 않는다.
- **ISP**: `Renderer`(표시)와 `InputProvider`(입력)를 하나의 거대한 인터페이스로
  묶지 않고 분리했다. `Step`도 화면(`render`), 검증(`validate`), 전이
  (`previous`/`apply`)로 나뉜 좁은 메서드만 요구한다.
- **DIP**: `app.py`는 `ConsoleRenderer`/`ConsoleInput`의 구체 클래스가 아니라
  프로토콜에 의존하며, 실제 구현은 생성 시점에 주입된다. 테스트는
  `tests/conftest.py`의 `FakeRenderer`/`FakeInput`을 주입해 `main()`의 전체
  입력 루프를 실제 stdin/stdout 없이 검증한다.

## 테스트 구성

| 파일 | 대상 |
|---|---|
| `tests/test_parts.py` | Enum 라벨 |
| `tests/test_selection.py` | `CarSelection` |
| `tests/test_rules.py` | 호환성 규칙 |
| `tests/test_actions.py` | 도메인 함수 (`select_*`, `run_produced_car`, `test_produced_car`) |
| `tests/test_steps.py` | `Step` 체인 조립, 범위 검증, `apply()` |
| `tests/test_io_adapters.py` | `ConsoleRenderer`/`ConsoleInput`/`delay` |
| `tests/test_app.py` | `CarAssemblyApp` 전체 시나리오 (E2E, fake I/O) |
| `tests/test_entrypoint.py` | `assemble.main()`이 `CarAssemblyApp`에 제대로 위임하는지 |
