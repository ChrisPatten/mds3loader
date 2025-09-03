"""Configuration handling for mds3loader."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment and CLI."""

    log_level: str = Field("INFO")
    sampling_factor: int = Field(1, ge=1, description="Process every Nth update.")
    exclusion_center_lat: float | None = Field(
        None, description="Center latitude for the exclusion zone."
    )
    exclusion_center_lon: float | None = Field(
        None, description="Center longitude for the exclusion zone."
    )
    exclusion_margin_deg: float = Field(
        0.0,
        ge=0.0,
        description="Half-size in degrees for the exclusion zone bounds.",
    )

    model_config = {
        "env_prefix": "MDS3_",
    }


def load_settings(**kwargs: str) -> Settings:
    """Return Settings populated from environment variables and overrides."""

    return Settings(**kwargs)
