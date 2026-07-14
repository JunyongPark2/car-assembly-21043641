import sys
import time
from typing import Protocol

CLEAR_SCREEN = "\033[H\033[2J"


class Renderer(Protocol):
    def show(self, text: str = "") -> None:
        ...

    def clear(self) -> None:
        ...


class InputProvider(Protocol):
    def read(self, prompt: str) -> str:
        ...


class ConsoleRenderer:
    def show(self, text: str = "") -> None:
        print(text)

    def clear(self) -> None:
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.flush()


class ConsoleInput:
    def read(self, prompt: str) -> str:
        return input(prompt)


def delay(ms: int) -> None:
    time.sleep(ms / 1000.0)
