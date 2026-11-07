"""
RetailPulse - Terminal Menu Integration Tests
Author: Kartikeya Pradhan
Subject: Python Programming (Semester 3)

Integration tests for the interactive terminal menu system, option routing,
error handling, dataset reloading, and exit behavior.
"""

from datetime import date
from io import StringIO
from pathlib import Path
import unittest
from unittest.mock import patch

from src.terminal_menu import (
    execute_menu_choice,
    run_terminal_menu,
    show_branch_performance_table,
    show_category_sales_table,
    show_customer_table,
    show_gross_income_table,
    show_kpi_summary_table,
    show_monthly_sales_table,
    show_payment_table,
    show_rating_table,
)


class TestTerminalMenuIntegration(unittest.TestCase):
    """Test suite for terminal menu routing, tables, and interaction handling."""

    def setUp(self):
        """Build sample records and path for controlled testing."""
        self.sample_path = Path("dataset/supermarket_sales.csv")
        self.sample_records = [
            {
                "Invoice ID": "INV-1001",
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
                "Invoice ID": "INV-1002",
                "Branch": "Cairo",
                "City": "Mandalay",
                "Customer type": "Normal",
                "Gender": "Male",
                "Product line": "Food and beverages",
                "Unit price": 20.0,
                "Quantity": 5,
                "Tax 5%": 5.0,
                "Sales": 105.0,
                "Date": date(2019, 2, 20),
                "YearMonth": "2019-02",
                "MonthName": "Feb 2019",
                "Payment": "Cash",
                "cogs": 100.0,
                "gross income": 5.0,
                "Rating": 7.0,
            },
        ]

    # --- Table Display Tests ---

    def test_show_kpi_summary_table(self):
        """KPI summary table outputs required metric lines."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            show_kpi_summary_table(self.sample_records)
            output = fake_out.getvalue()
            self.assertIn("EXECUTIVE KEY PERFORMANCE INDICATORS", output)
            self.assertIn("$210.00", output)
            self.assertIn("2", output)

    def test_show_monthly_sales_table(self):
        """Monthly sales table prints month rows and totals."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            show_monthly_sales_table(self.sample_records)
            output = fake_out.getvalue()
            self.assertIn("Jan 2019", output)
            self.assertIn("Feb 2019", output)

    def test_show_category_sales_table(self):
        """Category sales table prints product line rankings."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            show_category_sales_table(self.sample_records)
            output = fake_out.getvalue()
            self.assertIn("Electronic accessories", output)
            self.assertIn("Food and beverages", output)

    def test_show_branch_performance_table(self):
        """Branch table prints branch cities and figures."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            show_branch_performance_table(self.sample_records)
            output = fake_out.getvalue()
            self.assertIn("Branch Alex", output)
            self.assertIn("Branch Cairo", output)

    def test_show_payment_table(self):
        """Payment table outputs payment methods."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            show_payment_table(self.sample_records)
            output = fake_out.getvalue()
            self.assertIn("Ewallet", output)
            self.assertIn("Cash", output)

    def test_show_customer_table(self):
        """Customer table outputs Member and Normal types."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            show_customer_table(self.sample_records)
            output = fake_out.getvalue()
            self.assertIn("Member", output)
            self.assertIn("Normal", output)

    def test_show_gross_income_table(self):
        """Gross income table prints profit values."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            show_gross_income_table(self.sample_records)
            output = fake_out.getvalue()
            self.assertIn("GROSS INCOME (PROFIT)", output)

    def test_show_rating_table(self):
        """Rating table prints customer satisfaction scores."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            show_rating_table(self.sample_records)
            output = fake_out.getvalue()
            self.assertIn("CUSTOMER SATISFACTION RATING", output)

    # --- Menu Option Routing Tests (with Visualizer Mocks) ---

    @patch("src.terminal_menu.render_complete_dashboard")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_1_complete_dashboard(self, mock_pause, mock_render):
        """Option 1 calls render_complete_dashboard with records and show=True."""
        keep_running, _, _ = execute_menu_choice(1, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        mock_render.assert_called_once_with(self.sample_records, show=True)

    @patch("src.terminal_menu.plot_monthly_revenue_trend")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_2_monthly_trend(self, mock_pause, mock_plot):
        """Option 2 calls plot_monthly_revenue_trend."""
        keep_running, _, _ = execute_menu_choice(2, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        mock_plot.assert_called_once_with(self.sample_records, show=True)

    @patch("src.terminal_menu.plot_revenue_by_category")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_3_category_sales(self, mock_pause, mock_plot):
        """Option 3 calls plot_revenue_by_category."""
        keep_running, _, _ = execute_menu_choice(3, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        mock_plot.assert_called_once_with(self.sample_records, show=True)

    @patch("src.terminal_menu.plot_branch_performance")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_4_branch_performance(self, mock_pause, mock_plot):
        """Option 4 calls plot_branch_performance."""
        keep_running, _, _ = execute_menu_choice(4, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        mock_plot.assert_called_once_with(self.sample_records, show=True)

    @patch("src.terminal_menu.plot_payment_distribution")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_5_payment_distribution(self, mock_pause, mock_plot):
        """Option 5 calls plot_payment_distribution."""
        keep_running, _, _ = execute_menu_choice(5, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        mock_plot.assert_called_once_with(self.sample_records, show=True)

    @patch("src.terminal_menu.plot_customer_type_distribution")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_6_customer_distribution(self, mock_pause, mock_plot):
        """Option 6 calls plot_customer_type_distribution."""
        keep_running, _, _ = execute_menu_choice(6, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        mock_plot.assert_called_once_with(self.sample_records, show=True)

    @patch("src.terminal_menu.plot_gross_income_by_category")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_7_gross_income(self, mock_pause, mock_plot):
        """Option 7 calls plot_gross_income_by_category."""
        keep_running, _, _ = execute_menu_choice(7, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        mock_plot.assert_called_once_with(self.sample_records, show=True)

    @patch("src.terminal_menu.plot_rating_analysis")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_8_rating_analysis(self, mock_pause, mock_plot):
        """Option 8 calls plot_rating_analysis."""
        keep_running, _, _ = execute_menu_choice(8, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        mock_plot.assert_called_once_with(self.sample_records, show=True)

    def test_menu_option_10_exit(self):
        """Option 10 returns keep_running=False to terminate the application loop."""
        keep_running, _, _ = execute_menu_choice(10, self.sample_records, self.sample_path)
        self.assertFalse(keep_running)

    # --- Reload Dataset Functionality Tests ---

    @patch("builtins.input", return_value="")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_9_reload_current_file(self, mock_pause, mock_input):
        """Option 9 reloads dataset from disk when enter is pressed."""
        keep_running, new_records, new_path = execute_menu_choice(9, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        self.assertIsNotNone(new_records)
        self.assertEqual(len(new_records), 1000)
        self.assertEqual(new_path, self.sample_path)

    @patch("builtins.input", return_value="non_existent_file.csv")
    @patch("src.terminal_menu.pause_for_user")
    def test_menu_option_9_reload_missing_file_handled(self, mock_pause, mock_input):
        """Option 9 handles invalid or missing file paths gracefully without crashing."""
        keep_running, new_records, new_path = execute_menu_choice(9, self.sample_records, self.sample_path)
        self.assertTrue(keep_running)
        self.assertIsNone(new_records)
        self.assertIsNone(new_path)

    # --- Full Application Loop Tests ---

    @patch("builtins.input", return_value="10")
    def test_run_terminal_menu_immediate_exit(self, mock_input):
        """run_terminal_menu displays menu and exits cleanly on option 10."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            run_terminal_menu(self.sample_path)
            output = fake_out.getvalue()
            self.assertIn("RETAIL SALES ANALYTICS", output)
            self.assertIn("Thank you for using RetailPulse", output)

    @patch("builtins.input", side_effect=["invalid", "99", "10"])
    def test_run_terminal_menu_input_validation(self, mock_input):
        """Invalid choices are reported and rejected until a valid option is provided."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            run_terminal_menu(self.sample_path)
            output = fake_out.getvalue()
            self.assertIn("Invalid input 'invalid'", output)
            self.assertIn("Option 99 is out of range", output)
            self.assertIn("Thank you for using RetailPulse", output)

    @patch("builtins.input", return_value="q")
    def test_run_terminal_menu_missing_dataset_exit(self, mock_input):
        """Missing dataset prompt allows user to quit via 'q' cleanly."""
        with patch("sys.stdout", new=StringIO()):
            with self.assertRaises(SystemExit) as cm:
                run_terminal_menu(Path("missing/dataset.csv"))
            self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
