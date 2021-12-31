from types import SimpleNamespace

import pytest

from utils import CollegeMetricsDataStore, NoCollegeMetricsFoundError


def test_get_latest_none():
    CollegeMetricsDataStore.db = SimpleNamespace(
        college_metrics=SimpleNamespace(find_one=lambda *args, **kwargs: None)
    )

    with pytest.raises(NoCollegeMetricsFoundError):
        CollegeMetricsDataStore.get_latest()


def test_get_all_none():
    CollegeMetricsDataStore.db = SimpleNamespace(
        college_metrics=SimpleNamespace(
            find=lambda *args, **kwargs: SimpleNamespace(
                sort=lambda *args, **kwargs: None
            )
        )
    )

    with pytest.raises(NoCollegeMetricsFoundError):
        CollegeMetricsDataStore.get_all()
