from selection import CarSelection
from steps import build_first_step
from io_adapters import ConsoleRenderer, ConsoleInput, delay


class CarAssemblyApp:
    """Composition root: wires the console adapters (or fakes, for tests)
    to the Step chain. Nothing else in the codebase constructs
    ConsoleRenderer/ConsoleInput directly - depend on the Renderer/
    InputProvider protocols and let the caller decide the implementation."""

    def __init__(self, renderer=None, input_provider=None, delay_fn=None):
        self._renderer = renderer or ConsoleRenderer()
        self._input_provider = input_provider or ConsoleInput()
        self._delay = delay_fn or delay

    def run(self):
        selection = CarSelection()
        step = build_first_step()

        while True:
            self._renderer.clear()
            self._renderer.show(step.render())
            buf = self._input_provider.read("INPUT > ").strip()

            if buf == "exit":
                self._renderer.show("바이바이")
                break

            try:
                ans = int(buf)
            except ValueError:
                self._renderer.show("ERROR :: 숫자만 입력 가능")
                self._delay(800)
                continue

            error = step.validate(ans)
            if error:
                self._renderer.show(error)
                self._delay(800)
                continue

            if ans == 0:
                previous_step = step.previous()
                if previous_step is not None:
                    step = previous_step
                continue

            actions, step = step.apply(selection, ans)
            for message, ms in actions:
                self._renderer.show(message)
                self._delay(ms)
