# src/monitoring/telemetry.py
from ..utils.logger import logger
from typing import Dict, Any

def log_event(event_name: str, payload: Dict[str, Any] = None) -> None:
    logger.info("Telemetry event: %s | %s", event_name, payload or {})
