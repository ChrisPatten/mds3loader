"""Tests for aircraft sampling and exclusion logic."""

from mds3loader.config import Settings
from mds3loader.utils.aircraft import should_run_calculation


def test_sampling_factor_skips_updates() -> None:
    settings = Settings(sampling_factor=3)
    assert not should_run_calculation(0.0, 0.0, 1, settings)
    assert not should_run_calculation(0.0, 0.0, 2, settings)
    assert should_run_calculation(0.0, 0.0, 3, settings)


def test_exclusion_zone_prevents_calculation() -> None:
    settings = Settings(
        sampling_factor=1,
        exclusion_center_lat=10.0,
        exclusion_center_lon=20.0,
        exclusion_margin_deg=1.0,
    )
    # Inside exclusion zone -> skip
    assert not should_run_calculation(10.5, 20.5, 5, settings)
    # Outside exclusion zone -> process
    assert should_run_calculation(12.5, 23.5, 5, settings)

