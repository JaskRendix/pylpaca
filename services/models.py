from typing import Any

from pydantic import BaseModel, Field, model_validator


class DriverConfig(BaseModel):
    device_type: str
    device_number: int
    device_driver: str
    driver_config: dict[str, Any] = Field(default_factory=dict)

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class AscomConfigModel(BaseModel):
    drivers: list[DriverConfig]

    @model_validator(mode="after")
    def check_unique_device_numbers(self):
        seen = set()
        for d in self.drivers:
            key = (d.device_type, d.device_number)
            if key in seen:
                raise ValueError(f"Duplicate device: {key}")
            seen.add(key)
        return self
