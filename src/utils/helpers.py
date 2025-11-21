# src/utils/helpers.py
from pathlib import Path
import json
from typing import Any, Dict
from .logger import logger

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

def ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def write_json(rel_path: str, obj: Any) -> None:
    p = DATA_DIR / rel_path
    ensure_dir(p)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    logger.debug("Wrote JSON to %s", p)

def read_json(rel_path: str) -> Any:
    p = DATA_DIR / rel_path
    if not p.exists():
        raise FileNotFoundError(f"{p} not found")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def write_numpy_array(rel_path: str, arr) -> None:
    import numpy as _np
    p = DATA_DIR / rel_path
    ensure_dir(p)
    _np.save(p, arr)
    logger.debug("Wrote numpy array to %s", p)

def read_numpy_array(rel_path: str):
    import numpy as _np
    p = DATA_DIR / rel_path
    if not p.exists():
        raise FileNotFoundError(f"{p} not found")
    return _np.load(p)
