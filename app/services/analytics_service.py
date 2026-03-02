"""
Analytics Service

Provides descriptive financial metrics:
- Growth percentage
- Moving average
- Volatility
"""

import statistics

def calculate_analytics(prices):
    if not prices:
        return None
    values = [p.close_price for p in prices]

    latest = values[-1]
    first = values[0]

    growth = ((latest - first) / first) * 100 if first != 0 else 0

    window = min(len(values), 7)
    moving_avg = sum(values[-window:]) / window

    volatility = statistics.pstdev(values) if len(values) > 1 else 0

    return {
        "latest_price": round(latest, 2),
        "growth_percentage": round(growth, 2),
        "7_day_moving_average": round(moving_avg, 2),
        "volatility": round(volatility, 4),
        "data_points": len(values),
    }