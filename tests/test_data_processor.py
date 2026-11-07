"""
RetailPulse - Unit Test Suite
Author: Kartikeya Pradhan
Subject: Python Programming (Semester 3)

Tests for data loader and data processor modules using Python's standard
`unittest` framework with controlled in-memory sample records.
"""

from datetime import date, datetime
import unittest

from src.data_loader import (
    VERIFIED_COLUMNS,
    convert_record_types,
    validate_headers,
    validate_record,
)
from src.data_processor import (
    calculate_average_order_value,
    calculate_average_rating,
    calculate_kpis,
    calculate_total_gross_income,
    calculate_total_revenue,
    calculate_total_transactions,
    calculate_total_units_sold,
    get_branch_sales,
    get_category_gross_income,
    get_category_sales,
    get_customer_type_distribution,
    get_daily_sales,
    get_monthly_sales,
    get_payment_distribution,
    get_rating_analysis,
    get_top_categories,
)


class TestDataLoader(unittest.TestCase):
    """Test cases for validation and parsing logic in data_loader."""

    def test_validate_headers_success(self):
        """Header validation passes when all verified columns are present."""
        self.assertTrue(validate_headers(VERIFIED_COLUMNS))

    def test_validate_headers_missing_column(self):
        """Header validation raises ValueError if a column is missing."""
        incomplete = [c for c in VERIFIED_COLUMNS if c != "Sales"]
        with self.assertRaises(ValueError):
            validate_headers(incomplete)

    def test_validate_headers_empty(self):
        """Empty headers raise ValueError."""
        with self.assertRaises(ValueError):
            validate_headers([])

    def test_validate_record_success(self):
        """Valid row dictionary passes validation."""
        valid_row = {
            "Invoice ID": "101-00-1001",
            "Branch": "Alex",
            "City": "Yangon",
            "Customer type": "Member",
            "Gender": "Female",
            "Product line": "Electronic accessories",
            "Unit price": "50.00",
            "Quantity": "2",
            "Tax 5%": "5.00",
            "Sales": "105.00",
            "Date": "1/15/2019",
            "Time": "10:30:00 AM",
            "Payment": "Ewallet",
            "cogs": "100.00",
            "gross margin percentage": "4.7619",
            "gross income": "5.00",
            "Rating": "8.5",
        }
        self.assertTrue(validate_record(valid_row))

    def test_validate_record_negative_quantity(self):
        """Non-positive quantity raises ValueError."""
        invalid_row = {
            "Invoice ID": "101-00-1002",
            "Branch": "Alex",
            "Product line": "Food and beverages",
            "Unit price": "10.00",
            "Quantity": "0",  # Invalid quantity
            "Tax 5%": "0.50",
            "Sales": "10.50",
            "Date": "1/15/2019",
            "cogs": "10.00",
            "gross margin percentage": "4.76",
            "gross income": "0.50",
            "Rating": "7.0",
        }
        with self.assertRaises(ValueError):
            validate_record(invalid_row)

    def test_validate_record_invalid_rating(self):
        """Rating outside [0.0, 10.0] raises ValueError."""
        invalid_row = {
            "Invoice ID": "101-00-1003",
            "Branch": "Cairo",
            "Product line": "Fashion accessories",
            "Unit price": "20.00",
            "Quantity": "1",
            "Tax 5%": "1.00",
            "Sales": "21.00",
            "Date": "2/10/2019",
            "cogs": "20.00",
            "gross margin percentage": "4.76",
            "gross income": "1.00",
            "Rating": "12.5",  # Invalid rating > 10
        }
        with self.assertRaises(ValueError):
            validate_record(invalid_row)

    def test_validate_record_malformed_date(self):
        """Invalid date format raises ValueError."""
        invalid_row = {
            "Invoice ID": "101-00-1004",
            "Branch": "Giza",
            "Product line": "Sports and travel",
            "Unit price": "30.00",
            "Quantity": "1",
            "Tax 5%": "1.50",
            "Sales": "31.50",
            "Date": "2019/31/12",  # Malformed date
            "cogs": "30.00",
            "gross margin percentage": "4.76",
            "gross income": "1.50",
            "Rating": "9.0",
        }
        with self.assertRaises(ValueError):
            validate_record(invalid_row)

    def test_convert_record_types(self):
        """Record conversion casts strings to proper Python types."""
        raw = {
            "Invoice ID": "101-00-2001",
            "Branch": "Alex",
            "City": "Yangon",
            "Customer type": "Member",
            "Gender": "Male",
            "Product line": "Health and beauty",
            "Unit price": "25.50",
            "Quantity": "4",
            "Tax 5%": "5.10",
            "Sales": "107.10",
            "Date": "3/20/2019",
            "Time": "2:15:00 PM",
            "Payment": "Cash",
            "cogs": "102.00",
            "gross margin percentage": "4.7619",
            "gross income": "5.10",
            "Rating": "7.8",
        }
        converted = convert_record_types(raw)
        self.assertEqual(converted["Quantity"], 4)
        self.assertAlmostEqual(converted["Sales"], 107.10)
        self.assertAlmostEqual(converted["Unit price"], 25.50)
        self.assertEqual(converted["Date"], date(2019, 3, 20))
        self.assertEqual(converted["YearMonth"], "2019-03")
        self.assertEqual(converted["MonthName"], "Mar 2019")


class TestDataProcessor(unittest.TestCase):
    """Test cases for KPI calculations and business aggregations."""

    def setUp(self):
        """Set up controlled, deterministic sample data for tests."""
        self.sample_records = [
            {
                "Invoice ID": "INV-001",
                "Branch": "Alex",
                "City": "Yangon",
                "Customer type": "Member",
                "Gender": "Female",
                "Product line": "Electronic accessories",
                "Unit price": 50.0,
                "Quantity": 2,
                "Tax 5%": 5.0,
                "Sales": 105.0,
                "Date": date(2019, 1, 15),
                "YearMonth": "2019-01",
                "MonthName": "Jan 2019",
                "Payment": "Ewallet",
                "cogs": 100.0,
                "gross income": 5.0,
                "Rating": 8.0,
            },
            {
                "Invoice ID": "INV-002",
                "Branch": "Alex",
                "City": "Yangon",
                "Customer type": "Normal",
                "Gender": "Male",
                "Product line": "Food and beverages",
                "Unit price": 20.0,
                "Quantity": 5,
                "Tax 5%": 5.0,
                "Sales": 105.0,
                "Date": date(2019, 1, 20),
                "YearMonth": "2019-01",
                "MonthName": "Jan 2019",
                "Payment": "Cash",
                "cogs": 100.0,
                "gross income": 5.0,
                "Rating": 6.0,
            },
            {
                "Invoice ID": "INV-003",
                "Branch": "Cairo",
                "City": "Mandalay",
                "Customer type": "Member",
                "Gender": "Female",
                "Product line": "Electronic accessories",
                "Unit price": 100.0,
                "Quantity": 1,
                "Tax 5%": 5.0,
                "Sales": 105.0,
                "Date": date(2019, 2, 10),
                "YearMonth": "2019-02",
                "MonthName": "Feb 2019",
                "Payment": "Credit card",
                "cogs": 100.0,
                "gross income": 5.0,
                "Rating": 10.0,
            },
            {
                "Invoice ID": "INV-004",
                "Branch": "Giza",
                "City": "Naypyitaw",
                "Customer type": "Normal",
                "Gender": "Male",
                "Product line": "Sports and travel",
                "Unit price": 60.0,
                "Quantity": 3,
                "Tax 5%": 9.0,
                "Sales": 189.0,
                "Date": date(2019, 3, 5),
                "YearMonth": "2019-03",
                "MonthName": "Mar 2019",
                "Payment": "Cash",
                "cogs": 180.0,
                "gross income": 9.0,
                "Rating": 8.0,
            },
        ]

    # --- KPI Tests ---

    def test_calculate_kpis_controlled_data(self):
        """KPI calculation produces expected values for controlled data."""
        kpis = calculate_kpis(self.sample_records)
        # Expected totals:
        # Sales = 105 + 105 + 105 + 189 = 504.0
        # Transactions = 4
        # Units sold = 2 + 5 + 1 + 3 = 11
        # AOV = 504 / 4 = 126.0
        # Average Rating = (8 + 6 + 10 + 8) / 4 = 8.0
        # Gross Income = 5 + 5 + 5 + 9 = 24.0
        self.assertEqual(kpis["total_revenue"], 504.0)
        self.assertEqual(kpis["total_transactions"], 4)
        self.assertEqual(kpis["total_units_sold"], 11)
        self.assertEqual(kpis["average_order_value"], 126.0)
        self.assertEqual(kpis["average_rating"], 8.0)
        self.assertEqual(kpis["total_gross_income"], 24.0)

    def test_kpis_empty_dataset(self):
        """Empty record list returns zeros safely without ZeroDivisionError."""
        kpis = calculate_kpis([])
        self.assertEqual(kpis["total_revenue"], 0.0)
        self.assertEqual(kpis["total_transactions"], 0)
        self.assertEqual(kpis["total_units_sold"], 0)
        self.assertEqual(kpis["average_order_value"], 0.0)
        self.assertEqual(kpis["average_rating"], 0.0)
        self.assertEqual(kpis["total_gross_income"], 0.0)

    # --- Aggregation Tests ---

    def test_get_category_sales(self):
        """Category aggregation correctly groups and ranks revenue."""
        cat_sales = get_category_sales(self.sample_records)
        # Electronic accessories: 105 + 105 = 210.0
        # Sports and travel: 189.0
        # Food and beverages: 105.0
        self.assertEqual(cat_sales["Electronic accessories"], 210.0)
        self.assertEqual(cat_sales["Sports and travel"], 189.0)
        self.assertEqual(cat_sales["Food and beverages"], 105.0)

        # Verify sorted descending
        revenues = list(cat_sales.values())
        self.assertEqual(revenues, sorted(revenues, reverse=True))

    def test_get_monthly_sales_chronological(self):
        """Monthly aggregation groups and orders chronologically."""
        monthly = get_monthly_sales(self.sample_records)
        months = list(monthly.keys())
        self.assertEqual(months, ["2019-01", "2019-02", "2019-03"])
        self.assertEqual(monthly["2019-01"]["revenue"], 210.0)
        self.assertEqual(monthly["2019-01"]["transactions"], 2)
        self.assertEqual(monthly["2019-01"]["units_sold"], 7)
        self.assertEqual(monthly["2019-02"]["revenue"], 105.0)
        self.assertEqual(monthly["2019-03"]["revenue"], 189.0)

    def test_get_branch_sales(self):
        """Branch aggregation accurately aggregates per-branch figures."""
        branches = get_branch_sales(self.sample_records)
        self.assertIn("Alex", branches)
        self.assertIn("Cairo", branches)
        self.assertIn("Giza", branches)

        self.assertEqual(branches["Alex"]["revenue"], 210.0)
        self.assertEqual(branches["Alex"]["transactions"], 2)
        self.assertEqual(branches["Alex"]["units_sold"], 7)
        self.assertEqual(branches["Alex"]["gross_income"], 10.0)
        self.assertEqual(branches["Alex"]["average_order_value"], 105.0)
        self.assertEqual(branches["Alex"]["average_rating"], 7.0)

    def test_get_payment_distribution(self):
        """Payment distribution returns accurate counts and percentages."""
        pay = get_payment_distribution(self.sample_records)
        # Cash: 2 txns (50%)
        # Ewallet: 1 txn (25%)
        # Credit card: 1 txn (25%)
        self.assertEqual(pay["Cash"]["count"], 2)
        self.assertEqual(pay["Cash"]["percentage_count"], 50.0)
        self.assertEqual(pay["Ewallet"]["count"], 1)
        self.assertEqual(pay["Ewallet"]["percentage_count"], 25.0)
        self.assertEqual(pay["Credit card"]["count"], 1)
        self.assertEqual(pay["Credit card"]["percentage_count"], 25.0)

    def test_get_customer_type_distribution(self):
        """Customer type breakdown counts Member vs Normal."""
        cust = get_customer_type_distribution(self.sample_records)
        # Member: 2, Normal: 2 -> 50% each
        self.assertEqual(cust["Member"]["count"], 2)
        self.assertEqual(cust["Member"]["percentage_count"], 50.0)
        self.assertEqual(cust["Normal"]["count"], 2)
        self.assertEqual(cust["Normal"]["percentage_count"], 50.0)

    def test_get_category_gross_income(self):
        """Gross income per product category groups correctly."""
        income = get_category_gross_income(self.sample_records)
        self.assertEqual(income["Electronic accessories"], 10.0)
        self.assertEqual(income["Sports and travel"], 9.0)
        self.assertEqual(income["Food and beverages"], 5.0)

    def test_get_top_categories(self):
        """Top categories returns top N ranked items."""
        top_2 = get_top_categories(self.sample_records, n=2)
        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2[0], ("Electronic accessories", 210.0))
        self.assertEqual(top_2[1], ("Sports and travel", 189.0))

    def test_get_daily_sales(self):
        """Daily sales groups chronologically by calendar date."""
        daily = get_daily_sales(self.sample_records)
        self.assertEqual(daily["2019-01-15"], 105.0)
        self.assertEqual(daily["2019-01-20"], 105.0)
        self.assertEqual(daily["2019-02-10"], 105.0)
        self.assertEqual(daily["2019-03-05"], 189.0)

    def test_get_rating_analysis(self):
        """Rating analysis computes overall and per-category rating stats."""
        ratings = get_rating_analysis(self.sample_records)
        self.assertEqual(ratings["overall_average"], 8.0)
        self.assertEqual(ratings["by_category"]["Electronic accessories"]["average_rating"], 9.0)
        self.assertEqual(ratings["by_category"]["Food and beverages"]["average_rating"], 6.0)


if __name__ == "__main__":
    unittest.main()
