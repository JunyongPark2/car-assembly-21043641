import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class FakeInput:
    """Feeds a scripted sequence of answers, standing in for stdin."""

    def __init__(self, answers):
        self._answers = list(answers)

    def read(self, prompt):
        return self._answers.pop(0)


class FakeRenderer:
    """Collects every rendered frame instead of writing to stdout."""

    def __init__(self):
        self.frames = []
        self.clear_count = 0

    def show(self, text=""):
        self.frames.append(text)

    def clear(self):
        self.clear_count += 1
