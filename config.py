import json
from pathlib import Path
from types import SimpleNamespace

_raw = json.loads(Path(__file__).with_name("profile_config.json").read_text(encoding="utf-8"))
PROFILE = SimpleNamespace(**_raw["profile"])
THEMES = _raw["themes"]
