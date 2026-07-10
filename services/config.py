import json
import os
from pathlib import Path
from typing import Any

from .models import AscomConfigModel, DriverConfig


class AscomConfig:
    """
    Loads config.json once at startup and stores:
      • validated driver configuration (Pydantic models)
      • runtime driver instances (in memory)
    """

    def __init__(self, path: str | None = None):
        self.path = Path(path or os.getenv("PYLPACA_CONFIG_PATH", "config.json"))
        self._config_model: AscomConfigModel = self._load()
        self._drivers: dict[tuple[str, int], Any] = {}

    def _load(self) -> AscomConfigModel:
        with self.path.open() as f:
            raw = json.load(f)
        return AscomConfigModel(**raw)

    def all_driver_configs(self) -> list[DriverConfig]:
        """Return list of validated driver configs."""
        return self._config_model.drivers

    def get_driver_config(self, device_type: str, device_number: int):
        """Return the config model for a specific device."""
        for cfg in self._config_model.drivers:
            if cfg.device_type == device_type and cfg.device_number == device_number:
                return cfg
        return None

    def set_driver_instance(self, device_type: str, device_number: int, instance: Any):
        """Store a live driver instance in memory."""
        self._drivers[(device_type, device_number)] = instance

    def get_driver_instance(self, device_type: str, device_number: int):
        """Retrieve a previously instantiated driver."""
        key = (device_type, device_number)
        if key not in self._drivers:
            raise ValueError(f"No driver instance for {device_type} #{device_number}")
        return self._drivers[key]


ascom_config = AscomConfig()
