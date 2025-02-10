"""
    Contains the weights for the fundamental ratios and the scoring functions for the fundamental ratios.
    The weights are based on the 5-year, 4-quarter, and sector weights from the table.
"""

WEIGHTS_5_YEAR = {
    "pe_ratio": 0.10,
    "pb_ratio": 0.075,
    "de_ratio": 0.025,
    "roe": 0.05,
    "earnings_growth": 0.05,  # Earnings Growth Rate
}

WEIGHTS_4_QUARTER = {
    "pe_ratio": 0.10,
    "pb_ratio": 0.075,
    "de_ratio": 0.025,
    "roe": 0.05,
    "earnings_growth": 0.05,  # Earnings Growth Rate
}

WEIGHTS_SECTOR = {
    "pe_ratio": 0.05,
    "pb_ratio": 0.025,
    "de_ratio": 0.025,
    "roe": 0.05,
    "earnings_growth": 0.05,  # Earnings Growth Rate
}
# Technical Weight will be added later when we implement technical indicators


# --- Scoring Functions for Fundamental Ratios ---
def score_pe_ratio(pe_ratio):
    """Scores Price-to-Earnings Ratio. Lower P/E is generally better."""
    if pe_ratio is None:
        return 0
    if pe_ratio < 0:
        return 2
    if pe_ratio < 15:
        return 10
    elif 15 <= pe_ratio <= 25:
        return 5
    else:
        return 1


def score_pb_ratio(pb_ratio):
    """Scores Price-to-Book Ratio. Lower P/B is generally better."""
    if pb_ratio is None:
        return 0
    if pb_ratio < 1:
        return 10
    elif 1 <= pb_ratio <= 3:
        return 5
    else:
        return 1


def score_de_ratio(de_ratio):
    """Scores Debt-to-Equity Ratio. Lower D/E is generally better."""
    if de_ratio is None:
        return 0
    if de_ratio < 1:
        return 10
    elif 1 <= de_ratio <= 2:
        return 5
    else:
        return 1


def score_roe(roe):
    """Scores Return on Equity. Higher ROE is generally better."""
    if roe is None:
        return 0
    roe_percentage = roe * 100
    if roe_percentage > 15:
        return 10
    elif 10 <= roe_percentage <= 15:
        return 5
    else:
        return 1


def score_earnings_growth_rate(growth_rate):
    """Scores Earnings Growth Rate. Higher growth is better."""
    if growth_rate is None:
        return 0
    growth_percentage = growth_rate * 100
    if growth_percentage > 10:
        return 10
    elif 5 <= growth_percentage <= 10:
        return 5
    else:
        return 1
# --- End of Scoring Functions ---