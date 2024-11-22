"""Tests for data utility functions."""
import pytest
import pandas as pd
from utils.data_utils import merge_datasets
import streamlit as st

def test_merge_datasets(sample_mobility_data, sample_cost_data, monkeypatch):
    """Test merging mobility and cost datasets."""
    def mock_load_mobility():
        return sample_mobility_data
        
    def mock_load_cost():
        return sample_cost_data
    
    # Mock the data loading functions
    monkeypatch.setattr("utils.data_utils.load_mobility_data", mock_load_mobility)
    monkeypatch.setattr("utils.data_utils.load_cost_data", mock_load_cost)
    
    # Mock streamlit functions
    monkeypatch.setattr(st, "error", lambda x: None)
    
    # Test successful merge
    result = merge_datasets()
    assert result is not None
    assert len(result) == 5
    assert "sticker_price_2013" in result.columns
    assert "par_q1" in result.columns
    
    # Test data validation
    assert all(result["iclevel"] == 1)
    assert all(result["sticker_price_2013"] > 0)
    assert all(result["par_q1"] > 0)

def test_merge_datasets_with_missing_data(monkeypatch):
    """Test merging behavior when data is missing."""
    def mock_load_mobility():
        return None
        
    def mock_load_cost():
        return None
    
    # Mock the data loading functions
    monkeypatch.setattr("utils.data_utils.load_mobility_data", mock_load_mobility)
    monkeypatch.setattr("utils.data_utils.load_cost_data", mock_load_cost)
    
    # Mock streamlit functions
    monkeypatch.setattr(st, "error", lambda x: None)
    
    # Test handling of missing data
    result = merge_datasets()
    assert result is None
