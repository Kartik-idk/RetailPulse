"""
RetailPulse - Visualizer Smoke Tests
Author: Kartikeya Pradhan
Subject: Python Programming (Semester 3)

Smoke tests for all visualizer plotting functions and complete dashboard rendering
using a headless non-interactive backend (matplotlib Agg).
"""

from datetime import date
import unittest

import matplotlib
# Force headless Agg backend for automated tests
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.visualizer import (
    plot_branch_performance,
    plot_customer_type_distribution,
    plot_gross_income_by_category,
    plot_monthly_revenue_trend,
    plot_payment_distribution,
    plot_rating_analysis,
    plot_revenue_by_category,
    render_complete_dashboard,
)


class TestVisualizerSmoke(unittest.TestCase):
    """Smoke tests for individual charts and complete dashboard rendering."""

    def setUp(self):
        """Construct deterministic sample records."""
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
            {
                "Invoice ID": "INV-003",
                "Branch": "Giza",
                "City": "Naypyitaw",
                "Customer type": "Member",
                "Gender": "Female",
                "Product line": "Sports and travel",
                "Unit price": 60.0,
                "Quantity": 3,
                "Tax 5%": 9.0,
                "Sales": 189.0,
                "Date": date(2019, 3, 5),
                "YearMonth": "2019-03",
                "MonthName": "Mar 2019",
                "Payment": "Credit card",
                "cogs": 180.0,
                "gross income": 9.0,
                "Rating": 9.0,
            },
        ]

    def tearDown(self):
        """Ensure all figures are cleanly closed after each test."""
        plt.close("all")

    def test_plot_monthly_revenue_trend(self):
        """Monthly revenue trend chart executes cleanly."""
        fig, ax = plot_monthly_revenue_trend(self.sample_records, show=False)
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)
        self.assertEqual(ax.get_title(), "Monthly Revenue Trend")

    def test_plot_revenue_by_category(self):
        """Revenue by category horizontal bar chart executes cleanly."""
        fig, ax = plot_revenue_by_category(self.sample_records, show=False)
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(ax.get_title(), "Revenue by Product Category")

    def test_plot_branch_performance(self):
        """Branch performance chart executes cleanly."""
        fig, ax = plot_branch_performance(self.sample_records, show=False)
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(ax.get_title(), "Branch Performance & Revenue")

    def test_plot_payment_distribution(self):
        """Payment distribution donut chart executes cleanly."""
        fig, ax = plot_payment_distribution(self.sample_records, show=False)
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(ax.get_title(), "Payment Method Distribution")

    def test_plot_customer_type_distribution(self):
        """Customer type distribution donut chart executes cleanly."""
        fig, ax = plot_customer_type_distribution(self.sample_records, show=False)
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(ax.get_title(), "Customer Type Distribution")

    def test_plot_gross_income_by_category(self):
        """Gross income by category bar chart executes cleanly."""
        fig, ax = plot_gross_income_by_category(self.sample_records, show=False)
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(ax.get_title(), "Gross Income by Category")

    def test_plot_rating_analysis(self):
        """Rating analysis chart executes cleanly."""
        fig, ax = plot_rating_analysis(self.sample_records, show=False)
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(ax.get_title(), "Customer Rating by Product Category")

    def test_render_complete_dashboard(self):
        """Complete master dashboard renders all KPI cards and subplots."""
        fig = render_complete_dashboard(self.sample_records, show=False)
        self.assertIsInstance(fig, plt.Figure)
        # Dashboard must contain header + 5 KPI cards + 6 main charts = 12 axes
        self.assertGreaterEqual(len(fig.axes), 12)

    def test_empty_dataset_handling(self):
        """Visualizer functions handle empty records safely without raising exceptions."""
        fig1, ax1 = plot_monthly_revenue_trend([], show=False)
        fig2, ax2 = plot_revenue_by_category([], show=False)
        fig3, ax3 = plot_branch_performance([], show=False)
        fig4, ax4 = plot_payment_distribution([], show=False)
        fig5, ax5 = plot_customer_type_distribution([], show=False)
        fig6, ax6 = plot_gross_income_by_category([], show=False)
        fig7, ax7 = plot_rating_analysis([], show=False)
        fig8 = render_complete_dashboard([], show=False)

        for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8):
            self.assertIsInstance(f, plt.Figure)


if __name__ == "__main__":
    unittest.main()
