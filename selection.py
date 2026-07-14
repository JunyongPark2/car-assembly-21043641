from dataclasses import dataclass
from typing import Optional

from parts import CarType, EngineType, BrakeType, SteeringType


@dataclass
class CarSelection:
    """Owns the in-progress choice of parts, replacing the module-level
    q0-q3 globals assemble.py used to mutate directly."""

    car_type: Optional[CarType] = None
    engine: Optional[EngineType] = None
    brake: Optional[BrakeType] = None
    steering: Optional[SteeringType] = None

    def set_car_type(self, value: int) -> CarType:
        self.car_type = CarType(value)
        return self.car_type

    def set_engine(self, value: int) -> EngineType:
        self.engine = EngineType(value)
        return self.engine

    def set_brake(self, value: int) -> BrakeType:
        self.brake = BrakeType(value)
        return self.brake

    def set_steering(self, value: int) -> SteeringType:
        self.steering = SteeringType(value)
        return self.steering
