# utils/data_utils.py
"""Utility functions for data loading and processing."""
from typing import Optional
import pandas as pd
import streamlit as st
from utils.logger import app_logger
from pathlib import Path

# Define data file paths relative to project root
DATA_DIR = Path("data")
MOBILITY_FILE = DATA_DIR / "mrc_table2.csv"
COST_FILE = DATA_DIR / "mrc_table10.csv"

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_mobility_data() -> Optional[pd.DataFrame]:
    """Load and preprocess mobility data.
    
    Returns:
        Optional[pd.DataFrame]: Preprocessed mobility data or None if loading fails
    """
    try:
        app_logger.info(f"Loading mobility data from {MOBILITY_FILE}...")
        df = pd.read_csv(MOBILITY_FILE)
        app_logger.info(f"Successfully loaded mobility data with {len(df)} rows")
        return df
    except Exception as e:
        app_logger.error(f"Error loading mobility data: {str(e)}")
        st.error(f"Error loading mobility data: {str(e)}")
        return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_cost_data() -> Optional[pd.DataFrame]:
    """Load cost dataset with tuition information.
    
    Returns:
        Optional[pd.DataFrame]: Cost data or None if loading fails
    """
    try:
        app_logger.info(f"Loading cost data from {COST_FILE}...")
        df = pd.read_csv(COST_FILE)
        app_logger.info(f"Successfully loaded cost data with {len(df)} rows")
        return df
    except Exception as e:
        app_logger.error(f"Error loading cost data: {str(e)}")
        st.error(f"Error loading cost data: {str(e)}")
        return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def merge_datasets() -> Optional[pd.DataFrame]:
    """Merge mobility data with other relevant datasets.
    
    Returns:
        Optional[pd.DataFrame]: Merged dataset or None if merging fails
    """
    try:
        app_logger.info("Starting dataset merge...")
        mobility_df = load_mobility_data()
        cost_df = load_cost_data()
        
        if mobility_df is None or cost_df is None:
            app_logger.error("One or more required datasets failed to load")
            return None
            
        # Map iclevel values to standardized format
        # Original data: 1 = 4-year, 2 = 2-year
        # Our app: 4 = 4-year, 2 = 2-year
        mobility_df['iclevel'] = mobility_df['iclevel'].map({1: 4, 2: 2})
        cost_df['iclevel'] = cost_df['iclevel'].map({1: 4, 2: 2})
        
        # Keep only 2-year and 4-year colleges
        mobility_df = mobility_df[mobility_df['iclevel'].isin([2, 4])]
        cost_df = cost_df[cost_df['iclevel'].isin([2, 4])]
        
        app_logger.info(f"Filtered to {len(mobility_df)} mobility records and {len(cost_df)} cost records")
        
        merged_df = pd.merge(
            mobility_df,
            cost_df[['super_opeid', 'iclevel', 'sticker_price_2013', 'scorecard_netprice_2013']],
            on=['super_opeid', 'iclevel'],
            how='inner'
        )
        
        app_logger.info(f"Successfully merged datasets with {len(merged_df)} final records")
        return merged_df
    except Exception as e:
        app_logger.error(f"Error merging datasets: {str(e)}")
        st.error(f"Error merging datasets: {str(e)}")
        return None

def prepare_mobility_ladder(df: pd.DataFrame, selected_group: str = None) -> pd.DataFrame:
    """
    Prepare mobility ladder data showing probability distribution of child quintiles
    given parents in bottom quintile (Q1).
    
    Args:
        df: Input DataFrame with mobility data
        selected_group: Optional group filter (e.g., "Elite", "Selective Public")
        
    Returns:
        DataFrame with mobility ladder probabilities and descriptive labels
    """
    # Filter by group if specified
    if selected_group and selected_group != "All":
        df = df[df['tier_name'] == selected_group]
    
    # Calculate mean probabilities across institutions
    ladder_df = pd.DataFrame({
        'quintile': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5'],
        'probability': [
            df['kq1_cond_parq1'].mean(),
            df['kq2_cond_parq1'].mean(),
            df['kq3_cond_parq1'].mean(),
            df['kq4_cond_parq1'].mean(),
            df['kq5_cond_parq1'].mean()
        ],
        'description': [
            'Remain in Bottom Quintile',
            'Move to Lower Middle',
            'Move to Middle',
            'Move to Upper Middle',
            'Move to Top Quintile'
        ],
        'income_range': [
            'Bottom 20%',
            '20-40th percentile',
            '40-60th percentile',
            '60-80th percentile',
            'Top 20%'
        ]
    })
    
    # Verify probabilities sum to approximately 1
    total_prob = ladder_df['probability'].sum()
    if not 0.99 <= total_prob <= 1.01:
        app_logger.warning(f"Mobility ladder probabilities sum to {total_prob:.3f}, expected ~1.0")
    
    return ladder_df
