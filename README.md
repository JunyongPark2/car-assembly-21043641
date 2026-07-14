# car-assembly

콘솔에서 차량 타입(Sedan/SUV/Truck), 엔진, 제동장치, 조향장치를 순서대로
선택해 조립하고, 조합의 호환성을 RUN 또는 Test로 확인하는 대화형 CLI.

```
어떤 차량 타입을 선택할까요?
1. Sedan
2. SUV
3. Truck
```

## 요구 사항

- Python 3.9 이상 (개발/테스트는 3.14 기준)
- 표준 라이브러리 외 실행 의존성 없음 (테스트에만 `pytest` 필요)

## 실행

```bash
python assemble.py
```

각 화면에서 번호를 입력해 진행하고, `0`으로 이전 화면으로 돌아가며,
`exit`을 입력하면 종료한다.

## 개발 환경 설정

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov
```

## 테스트

```bash
pytest
```

## 프로젝트 구조

```
car-assembly/
├── assemble.py        # 실행 진입점
├── car_assembly/       # 도메인/애플리케이션 패키지
│   ├── parts.py         # 부품 Enum (CarType/EngineType/BrakeType/SteeringType)
│   ├── selection.py      # CarSelection 값 객체
│   ├── rules.py         # 부품 호환성 규칙
│   ├── actions.py       # 선택/조립/테스트 도메인 로직
│   ├── steps.py         # 마법사 단계(Step) 상태 머신
│   ├── io_adapters.py    # 콘솔 입출력 어댑터
│   └── app.py           # CarAssemblyApp (합성근)
├── tests/              # pytest 테스트
└── docs/               # 설계 문서
```

모듈별 책임과 의존 관계, SOLID 원칙이 어디에 반영되었는지는
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)를 참고.

## 문서

- [`docs/ANALYSIS.md`](docs/ANALYSIS.md) — 리팩토링 전 코드 분석 (역사적 기록)
- [`docs/PLAN.md`](docs/PLAN.md) — Phase별 리팩토링 계획
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — 리팩토링 후 최종 아키텍처
