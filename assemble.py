from selection import CarSelection
from steps import build_first_step
from io_adapters import ConsoleRenderer, ConsoleInput, delay


def main(renderer=None, input_provider=None, delay_fn=None):
    renderer = renderer or ConsoleRenderer()
    input_provider = input_provider or ConsoleInput()
    delay_fn = delay_fn or delay

    selection = CarSelection()
    step = build_first_step()

    while True:
        renderer.clear()
        renderer.show(step.render())
        buf = input_provider.read("INPUT > ").strip()

        if buf == "exit":
            renderer.show("바이바이")
            break

        try:
            ans = int(buf)
        except ValueError:
            renderer.show("ERROR :: 숫자만 입력 가능")
            delay_fn(800)
            continue

        error = step.validate(ans)
        if error:
            renderer.show(error)
            delay_fn(800)
            continue

        if ans == 0:
            previous_step = step.previous()
            if previous_step is not None:
                step = previous_step
            continue

        actions, step = step.apply(selection, ans)
        for message, ms in actions:
            renderer.show(message)
            delay_fn(ms)


if __name__ == "__main__":
    main()
