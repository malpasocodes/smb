"""Configuration settings for the College Mobility Analysis Dashboard."""

# Institution tier mappings
TIER_MAP = {
    1: "Ivy Plus",
    2: "Other elite schools",
    3: "Highly selective public",
    4: "Highly selective private",
    5: "Selective public",
    6: "Selective private",
    7: "Nonselective 4-year public",
    8: "Nonselective 4-year private",
    9: "Two-year (public and private)",
    10: "Four-year for-profit"
}

# Filter configurations
FILTER_CONFIG = {
    "min_q1_students": {
        "min_value": 0,
        "max_value": 50,
        "default": 5,
        "step": 1
    }
}

# Institution grouping configurations
INSTITUTION_GROUPS = {
    "Elite": [1, 2],
    "Highly Selective": [3, 4],
    "Selective": [5, 6],
    "Nonselective": [7, 8],
    "For-profit": [10]
}
