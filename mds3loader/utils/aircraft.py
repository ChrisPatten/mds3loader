"""Utilities for managing aircraft update calculations."""

from __future__ import annotations

from dataclasses import dataclass

from mds3loader.config import Settings


@dataclass
class ExclusionZone:
    """Square exclusion zone defined around a center point."""

    center_lat: float
    center_lon: float
    margin_deg: float

    def contains(self, lat: float, lon: float) -> bool:
        """Return True if a point lies inside the exclusion zone."""

        return (
            self.center_lat - self.margin_deg <= lat <= self.center_lat + self.margin_deg
            and self.center_lon - self.margin_deg
            <= lon
            <= self.center_lon + self.margin_deg
        )


def should_run_calculation(
    lat: float, lon: float, update: int, settings: Settings
) -> bool:
    """Return True if an update should trigger a heavy calculation.

    Args:
        lat: Aircraft latitude.
        lon: Aircraft longitude.
        update: Sequential update number (starting from 1).
        settings: Application configuration.

    The calculation is skipped when the aircraft is inside the exclusion zone
    or when the sampling factor does not select the current update.
    """

    if (
        settings.exclusion_center_lat is not None
        and settings.exclusion_center_lon is not None
        and settings.exclusion_margin_deg > 0
    ):
        zone = ExclusionZone(
            settings.exclusion_center_lat,
            settings.exclusion_center_lon,
            settings.exclusion_margin_deg,
        )
        if zone.contains(lat, lon):
            return False

    return update % settings.sampling_factor == 0

