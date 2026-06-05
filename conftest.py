import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from unit_converter.infrastructure.config_loader import default_registry as load_default_registry


@pytest.fixture
def default_registry():
    """Shared registry SSOT — loads ratios from config/units.json."""
    return load_default_registry()
