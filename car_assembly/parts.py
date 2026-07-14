from enum import Enum


class CarType(Enum):
    SEDAN = 1
    SUV = 2
    TRUCK = 3

    @property
    def label(self):
        return _CAR_TYPE_LABELS[self]


class EngineType(Enum):
    GM = 1
    TOYOTA = 2
    WIA = 3
    BROKEN = 4

    @property
    def label(self):
        return _ENGINE_LABELS[self]


class BrakeType(Enum):
    MANDO = 1
    CONTINENTAL = 2
    BOSCH = 3

    @property
    def label(self):
        return _BRAKE_LABELS[self]


class SteeringType(Enum):
    BOSCH = 1
    MOBIS = 2

    @property
    def label(self):
        return _STEERING_LABELS[self]


_CAR_TYPE_LABELS = {
    CarType.SEDAN: "Sedan",
    CarType.SUV: "SUV",
    CarType.TRUCK: "Truck",
}

_ENGINE_LABELS = {
    EngineType.GM: "GM",
    EngineType.TOYOTA: "TOYOTA",
    EngineType.WIA: "WIA",
    EngineType.BROKEN: "고장난 엔진",
}

_BRAKE_LABELS = {
    BrakeType.MANDO: "Mando",
    BrakeType.CONTINENTAL: "Continental",
    BrakeType.BOSCH: "Bosch",
}

_STEERING_LABELS = {
    SteeringType.BOSCH: "Bosch",
    SteeringType.MOBIS: "Mobis",
}
