import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

import assemble


@pytest.fixture(autouse=True)
def reset_globals():
    """assemble.py keeps selection state in module-level globals (q0-q3);
    reset them before every test so tests don't leak state into each other."""
    assemble.q0 = None
    assemble.q1 = None
    assemble.q2 = None
    assemble.q3 = None
    assemble.q4 = None
    yield
