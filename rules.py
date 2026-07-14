from typing import List, Optional, Protocol

from parts import CarType, EngineType, BrakeType, SteeringType
from selection import CarSelection


class CompatibilityRule(Protocol):
    def check(self, selection: CarSelection) -> Optional[str]:
        """Return a failure message if the rule is violated, else None."""
        ...


class _PredicateRule:
    """A compatibility rule expressed as a predicate + its failure message,
    so a new rule is just one new instance, not a new elif branch."""

    def __init__(self, predicate, message: str):
        self._predicate = predicate
        self._message = message

    def check(self, selection: CarSelection) -> Optional[str]:
        if self._predicate(selection):
            return self._message
        return None


COMPATIBILITY_RULES: List[CompatibilityRule] = [
    _PredicateRule(
        lambda s: s.car_type == CarType.SEDAN and s.brake == BrakeType.CONTINENTAL,
        "Sedan에는 Continental제동장치 사용 불가",
    ),
    _PredicateRule(
        lambda s: s.car_type == CarType.SUV and s.engine == EngineType.TOYOTA,
        "SUV에는 TOYOTA엔진 사용 불가",
    ),
    _PredicateRule(
        lambda s: s.car_type == CarType.TRUCK and s.engine == EngineType.WIA,
        "Truck에는 WIA엔진 사용 불가",
    ),
    _PredicateRule(
        lambda s: s.car_type == CarType.TRUCK and s.brake == BrakeType.MANDO,
        "Truck에는 Mando제동장치 사용 불가",
    ),
    _PredicateRule(
        lambda s: s.brake == BrakeType.BOSCH and s.steering != SteeringType.BOSCH,
        "Bosch제동장치에는 Bosch조향장치 이외 사용 불가",
    ),
]


def find_violations(selection: CarSelection) -> List[str]:
    """Evaluate every rule once; both a pass/fail check and a detailed
    failure message can be derived from this single source of truth."""
    violations = []
    for rule in COMPATIBILITY_RULES:
        message = rule.check(selection)
        if message is not None:
            violations.append(message)
    return violations
