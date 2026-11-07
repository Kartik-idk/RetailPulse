"""
RetailPulse - Data Processor Module
Author: Kartikeya Pradhan
Subject: Python Programming (Semester 3)

This module implements all core retail analytics, Key Performance Indicators (KPIs),
and aggregation logic. It uses core Python concepts: native loops, dictionaries,
lists, conditionals, and standard mathematical operations.
No external data science libraries (Pandas / NumPy) are used.
"""

from typing import Any, Dict, List, Optional, Tuple


# -----------------------------------------------------------------------------
# Individual KPI Functions
# -----------------------------------------------------------------------------

def calculate_total_revenue(records: List[Dict[str, Any]]) -> float:
    """
    Calculate the sum of all transaction sales revenue.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        float: Total revenue rounded to 2 decimal places (or 0.0 if empty).
    """
    if not records:
        return 0.0
    total = sum(record.get("Sales", 0.0) for record in records)
    return round(total, 2)


def calculate_total_transactions(records: List[Dict[str, Any]]) -> int:
    """
    Count the total number of transactions in the dataset.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        int: Total number of valid transactions.
    """
    return len(records)


def calculate_total_units_sold(records: List[Dict[str, Any]]) -> int:
    """
    Calculate the sum of all product quantities sold.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        int: Total units sold across all transactions.
    """
    if not records:
        return 0
    return sum(record.get("Quantity", 0) for record in records)


def calculate_average_order_value(records: List[Dict[str, Any]]) -> float:
    """
    Calculate the Average Order Value (AOV = Total Revenue / Total Transactions).

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        float: Average order value rounded to 2 decimal places (or 0.0 if empty).
    """
    if not records:
        return 0.0
    total_rev = calculate_total_revenue(records)
    return round(total_rev / len(records), 2)


def calculate_average_rating(records: List[Dict[str, Any]]) -> float:
    """
    Calculate the average customer satisfaction rating.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        float: Average rating rounded to 2 decimal places (or 0.0 if empty).
    """
    if not records:
        return 0.0
    ratings = [record.get("Rating", 0.0) for record in records if "Rating" in record]
    if not ratings:
        return 0.0
    return round(sum(ratings) / len(ratings), 2)


def calculate_total_gross_income(records: List[Dict[str, Any]]) -> float:
    """
    Calculate the total gross income generated across all transactions.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        float: Total gross income rounded to 2 decimal places (or 0.0 if empty).
    """
    if not records:
        return 0.0
    total = sum(record.get("gross income", 0.0) for record in records)
    return round(total, 2)


def calculate_kpis(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute a consolidated dictionary of all Key Performance Indicators.

    KPIs computed:
        - Total Revenue
        - Total Transactions
        - Total Units Sold
        - Average Order Value
        - Average Customer Rating
        - Total Gross Income

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        Dict[str, Any]: Key-value mapping of each KPI metric.
    """
    return {
        "total_revenue": calculate_total_revenue(records),
        "total_transactions": calculate_total_transactions(records),
        "total_units_sold": calculate_total_units_sold(records),
        "average_order_value": calculate_average_order_value(records),
        "average_rating": calculate_average_rating(records),
        "total_gross_income": calculate_total_gross_income(records),
    }


# -----------------------------------------------------------------------------
# Aggregation Functions
# -----------------------------------------------------------------------------

def get_category_sales(
    records: List[Dict[str, Any]],
    sort_descending: bool = True,
) -> Dict[str, float]:
    """
    Aggregate total sales revenue grouped by Product line.

    Args:
        records: List of cleaned transactional record dictionaries.
        sort_descending: If True, returns dictionary sorted by revenue in descending order.

    Returns:
        Dict[str, float]: Mapping of Product line -> total sales revenue.
    """
    category_totals: Dict[str, float] = {}

    for record in records:
        category = record.get("Product line", "Unknown")
        amount = record.get("Sales", 0.0)
        category_totals[category] = category_totals.get(category, 0.0) + amount

    for cat in category_totals:
        category_totals[cat] = round(category_totals[cat], 2)

    if sort_descending:
        sorted_pairs = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_pairs)

    return category_totals


def get_monthly_sales(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Aggregate sales revenue, transaction count, and units sold chronologically by month.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        Dict[str, Dict[str, Any]]: Chronologically sorted dictionary keyed by 'YYYY-MM',
        containing 'label' (e.g. 'Jan 2019'), 'revenue', 'transactions', and 'units_sold'.
    """
    monthly: Dict[str, Dict[str, Any]] = {}

    for record in records:
        year_month = record.get("YearMonth")
        if not year_month:
            # Fallback if YearMonth wasn't pre-computed
            date_val = record.get("Date")
            if hasattr(date_val, "strftime"):
                year_month = date_val.strftime("%Y-%m")
                label = date_val.strftime("%b %Y")
            else:
                continue
        else:
            label = record.get("MonthName", year_month)

        amount = record.get("Sales", 0.0)
        qty = record.get("Quantity", 0)

        if year_month not in monthly:
            monthly[year_month] = {
                "label": label,
                "revenue": 0.0,
                "transactions": 0,
                "units_sold": 0,
            }

        monthly[year_month]["revenue"] += amount
        monthly[year_month]["transactions"] += 1
        monthly[year_month]["units_sold"] += qty

    # Sort keys chronologically
    sorted_keys = sorted(monthly.keys())
    result: Dict[str, Dict[str, Any]] = {}

    for ym in sorted_keys:
        info = monthly[ym]
        result[ym] = {
            "label": info["label"],
            "revenue": round(info["revenue"], 2),
            "transactions": info["transactions"],
            "units_sold": info["units_sold"],
        }

    return result


def get_branch_sales(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Aggregate operational and sales metrics grouped by supermarket Branch.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        Dict[str, Dict[str, Any]]: Branch identifier -> {
            'city', 'revenue', 'transactions', 'units_sold', 'gross_income',
            'average_order_value', 'average_rating'
        }
    """
    branch_map: Dict[str, Dict[str, Any]] = {}

    for record in records:
        branch = record.get("Branch", "Unknown")
        city = record.get("City", "")
        amount = record.get("Sales", 0.0)
        qty = record.get("Quantity", 0)
        income = record.get("gross income", 0.0)
        rating = record.get("Rating", 0.0)

        if branch not in branch_map:
            branch_map[branch] = {
                "city": city,
                "revenue": 0.0,
                "transactions": 0,
                "units_sold": 0,
                "gross_income": 0.0,
                "rating_sum": 0.0,
            }

        branch_map[branch]["revenue"] += amount
        branch_map[branch]["transactions"] += 1
        branch_map[branch]["units_sold"] += qty
        branch_map[branch]["gross_income"] += income
        branch_map[branch]["rating_sum"] += rating

    result: Dict[str, Dict[str, Any]] = {}
    for branch, data in branch_map.items():
        count = data["transactions"]
        avg_rating = round(data["rating_sum"] / count, 2) if count > 0 else 0.0
        aov = round(data["revenue"] / count, 2) if count > 0 else 0.0

        result[branch] = {
            "city": data["city"],
            "revenue": round(data["revenue"], 2),
            "transactions": count,
            "units_sold": data["units_sold"],
            "gross_income": round(data["gross_income"], 2),
            "average_order_value": aov,
            "average_rating": avg_rating,
        }

    return dict(sorted(result.items()))


def get_payment_distribution(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Aggregate volume, revenue, and relative percentage for each payment method.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        Dict[str, Dict[str, Any]]: Payment method -> {
            'count', 'revenue', 'percentage_count', 'percentage_revenue'
        }
    """
    payment_map: Dict[str, Dict[str, Any]] = {}
    total_txns = len(records)
    total_rev = calculate_total_revenue(records)

    for record in records:
        method = record.get("Payment", "Unknown")
        amount = record.get("Sales", 0.0)

        if method not in payment_map:
            payment_map[method] = {"count": 0, "revenue": 0.0}

        payment_map[method]["count"] += 1
        payment_map[method]["revenue"] += amount

    result: Dict[str, Dict[str, Any]] = {}
    for method, data in payment_map.items():
        pct_count = round((data["count"] / total_txns) * 100, 2) if total_txns > 0 else 0.0
        pct_rev = round((data["revenue"] / total_rev) * 100, 2) if total_rev > 0 else 0.0

        result[method] = {
            "count": data["count"],
            "revenue": round(data["revenue"], 2),
            "percentage_count": pct_count,
            "percentage_revenue": pct_rev,
        }

    # Sort by transaction count descending
    return dict(sorted(result.items(), key=lambda item: item[1]["count"], reverse=True))


def get_customer_type_distribution(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Aggregate volume, revenue, and percentage metrics grouped by Customer type.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        Dict[str, Dict[str, Any]]: Customer type -> {
            'count', 'revenue', 'percentage_count', 'percentage_revenue'
        }
    """
    cust_map: Dict[str, Dict[str, Any]] = {}
    total_txns = len(records)
    total_rev = calculate_total_revenue(records)

    for record in records:
        cust_type = record.get("Customer type", "Unknown")
        amount = record.get("Sales", 0.0)

        if cust_type not in cust_map:
            cust_map[cust_type] = {"count": 0, "revenue": 0.0}

        cust_map[cust_type]["count"] += 1
        cust_map[cust_type]["revenue"] += amount

    result: Dict[str, Dict[str, Any]] = {}
    for cust_type, data in cust_map.items():
        pct_count = round((data["count"] / total_txns) * 100, 2) if total_txns > 0 else 0.0
        pct_rev = round((data["revenue"] / total_rev) * 100, 2) if total_rev > 0 else 0.0

        result[cust_type] = {
            "count": data["count"],
            "revenue": round(data["revenue"], 2),
            "percentage_count": pct_count,
            "percentage_revenue": pct_rev,
        }

    return dict(sorted(result.items(), key=lambda item: item[1]["count"], reverse=True))


def get_category_gross_income(
    records: List[Dict[str, Any]],
    sort_descending: bool = True,
) -> Dict[str, float]:
    """
    Aggregate gross income grouped by Product line category.

    Args:
        records: List of cleaned transactional record dictionaries.
        sort_descending: If True, returns dictionary sorted by income descending.

    Returns:
        Dict[str, float]: Product line -> total gross income.
    """
    income_map: Dict[str, float] = {}

    for record in records:
        cat = record.get("Product line", "Unknown")
        income = record.get("gross income", 0.0)
        income_map[cat] = income_map.get(cat, 0.0) + income

    for cat in income_map:
        income_map[cat] = round(income_map[cat], 2)

    if sort_descending:
        sorted_pairs = sorted(income_map.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_pairs)

    return income_map


def get_top_categories(
    records: List[Dict[str, Any]],
    n: Optional[int] = 5,
) -> List[Tuple[str, float]]:
    """
    Rank product categories by total sales revenue.

    Args:
        records: List of cleaned transactional record dictionaries.
        n: Number of top categories to return. If None, returns all categories.

    Returns:
        List[Tuple[str, float]]: List of (category, revenue) pairs sorted descending.
    """
    category_sales = get_category_sales(records, sort_descending=True)
    ranked = list(category_sales.items())
    if n is not None:
        return ranked[:n]
    return ranked


def get_daily_sales(records: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Aggregate total revenue by calendar day, chronologically sorted.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        Dict[str, float]: 'YYYY-MM-DD' date string -> total day's revenue.
    """
    daily: Dict[str, float] = {}

    for record in records:
        date_obj = record.get("Date")
        if hasattr(date_obj, "strftime"):
            date_key = date_obj.strftime("%Y-%m-%d")
        else:
            date_key = str(date_obj)

        amount = record.get("Sales", 0.0)
        daily[date_key] = daily.get(date_key, 0.0) + amount

    sorted_dates = sorted(daily.keys())
    return {d: round(daily[d], 2) for d in sorted_dates}


def get_rating_analysis(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate customer rating statistics overall and broken down by category.

    Args:
        records: List of cleaned transactional record dictionaries.

    Returns:
        Dict[str, Any]: Contains 'overall_average' and 'by_category' breakdown.
    """
    if not records:
        return {"overall_average": 0.0, "by_category": {}}

    cat_ratings: Dict[str, List[float]] = {}
    all_ratings: List[float] = []

    for record in records:
        rating = record.get("Rating")
        if rating is not None:
            all_ratings.append(rating)
            cat = record.get("Product line", "Unknown")
            if cat not in cat_ratings:
                cat_ratings[cat] = []
            cat_ratings[cat].append(rating)

    overall_avg = round(sum(all_ratings) / len(all_ratings), 2) if all_ratings else 0.0

    by_category: Dict[str, Dict[str, Any]] = {}
    for cat, ratings in cat_ratings.items():
        by_category[cat] = {
            "average_rating": round(sum(ratings) / len(ratings), 2),
            "count": len(ratings),
            "min_rating": min(ratings),
            "max_rating": max(ratings),
        }

    return {
        "overall_average": overall_avg,
        "by_category": dict(sorted(by_category.items())),
    }
