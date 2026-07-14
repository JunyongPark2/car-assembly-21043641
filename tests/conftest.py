import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

import assemble


@pytest.fixture(autouse=True)
def reset_globals():
    """assemble.py keeps selection state in module-level globals (q0-q3);
    reset them before every test so tests don't leak state into each other."""
    assemble.q0 = 0
    assemble.q1 = 0
    assemble.q2 = 0
    assemble.q3 = 0
    assemble.q4 = 0
    yield
