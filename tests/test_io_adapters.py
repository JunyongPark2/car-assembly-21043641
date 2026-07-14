import time

from car_assembly.io_adapters import ConsoleRenderer, ConsoleInput, delay


def test_console_renderer_show_prints_text(capsys):
    ConsoleRenderer().show("hello")
    assert capsys.readouterr().out == "hello\n"


def test_console_renderer_clear_writes_ansi_escape(capsys):
    ConsoleRenderer().clear()
    assert capsys.readouterr().out == "\033[H\033[2J"


def test_console_input_reads_from_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "typed")
    assert ConsoleInput().read("INPUT > ") == "typed"


def test_delay_sleeps_for_given_milliseconds(monkeypatch):
    recorded = []
    monkeypatch.setattr(time, "sleep", lambda seconds: recorded.append(seconds))
    delay(500)
    assert recorded == [0.5]
