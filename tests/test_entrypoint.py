from assemble import main
from conftest import FakeInput, FakeRenderer


def test_main_delegates_to_car_assembly_app():
    """assemble.main() is a thin wrapper around CarAssemblyApp - this pins
    that the wrapper still forwards renderer/input_provider/delay_fn."""
    renderer = FakeRenderer()
    main(renderer=renderer, input_provider=FakeInput(["exit"]), delay_fn=lambda ms: None)
    assert "바이바이" in renderer.frames
