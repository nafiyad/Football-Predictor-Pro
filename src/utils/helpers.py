"""Helper utility functions."""
from datetime import datetime, timedelta
from typing import Optional, Tuple


def format_date(date: datetime, format_str: str = "%d %b %Y") -> str:
    """Format datetime to string."""
    return date.strftime(format_str)


def format_time(date: datetime, format_str: str = "%H:%M") -> str:
    """Format datetime to time string."""
    return date.strftime(format_str)


def calculate_odds_from_probability(probability: float) -> float:
    """
    Calculate decimal odds from probability.
    
    Args:
        probability: Probability between 0 and 1
        
    Returns:
        Decimal odds
    """
    if probability <= 0 or probability >= 1:
        return 1.01
    return round(1 / probability, 2)


def calculate_probability_from_odds(odds: float) -> float:
    """
    Calculate probability from decimal odds.
    
    Args:
        odds: Decimal odds
        
    Returns:
        Probability between 0 and 1
    """
    if odds <= 1:
        return 0.99
    return round(1 / odds, 4)


def calculate_roi(total_stake: float, total_return: float) -> float:
    """
    Calculate Return on Investment (ROI).
    
    Args:
        total_stake: Total amount staked
        total_return: Total amount returned
        
    Returns:
        ROI as percentage
    """
    if total_stake == 0:
        return 0.0
    return round(((total_return - total_stake) / total_stake) * 100, 2)


def get_form_string(results: list) -> str:
    """
    Convert list of results to form string.
    
    Args:
        results: List of 'W', 'D', 'L'
        
    Returns:
        Form string like "WWDLW"
    """
    return ''.join(results[-5:])  # Last 5 results


def get_confidence_level(confidence: float) -> Tuple[str, str]:
    """
    Get confidence level and color based on confidence score.
    
    Args:
        confidence: Confidence score between 0 and 1
        
    Returns:
        Tuple of (level_name, color_code)
    """
    if confidence >= 0.70:
        return ("High", "#2ecc71")  # Green
    elif confidence >= 0.55:
        return ("Medium", "#f39c12")  # Orange
    else:
        return ("Low", "#e74c3c")  # Red


def get_result_from_score(home_goals: int, away_goals: int) -> str:
    """
    Get match result (1, X, 2) from score.
    
    Args:
        home_goals: Home team goals
        away_goals: Away team goals
        
    Returns:
        '1' for home win, 'X' for draw, '2' for away win
    """
    if home_goals > away_goals:
        return '1'
    elif home_goals == away_goals:
        return 'X'
    else:
        return '2'


def check_btts(home_goals: int, away_goals: int) -> bool:
    """Check if both teams scored."""
    return home_goals > 0 and away_goals > 0


def check_over_under(total_goals: int, line: float = 2.5) -> str:
    """
    Check if total goals is over or under the line.
    
    Args:
        total_goals: Total goals in match
        line: Over/Under line
        
    Returns:
        'Over' or 'Under'
    """
    return 'Over' if total_goals > line else 'Under'


def get_date_range(days: int = 7) -> Tuple[datetime, datetime]:
    """
    Get date range from today.
    
    Args:
        days: Number of days
        
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def percentage_to_string(value: float, decimals: int = 1) -> str:
    """Convert decimal to percentage string."""
    return f"{value * 100:.{decimals}f}%"



