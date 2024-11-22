"""Pytest configuration and fixtures."""
import pytest
import pandas as pd
import os

@pytest.fixture
def sample_mobility_data():
    """Create sample mobility data for testing."""
    return pd.DataFrame({
        'super_opeid': range(1, 6),
        'iclevel': [1] * 5,
        'par_q1': [0.1, 0.2, 0.05, 0.15, 0.25],
        'kq4_cond_parq1': [0.2, 0.3, 0.1, 0.25, 0.35],
        'kq5_cond_parq1': [0.1, 0.15, 0.05, 0.12, 0.18],
        'tier': [1, 2, 3, 4, 5]
    })

@pytest.fixture
def sample_cost_data():
    """Create sample cost data for testing."""
    return pd.DataFrame({
        'super_opeid': range(1, 6),
        'iclevel': [1] * 5,
        'sticker_price_2013': [50000, 45000, 30000, 35000, 40000],
        'scorecard_netprice_2013': [30000, 25000, 20000, 22000, 24000]
    })

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory with test data files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir
