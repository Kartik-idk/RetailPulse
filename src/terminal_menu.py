"""
RetailPulse - Interactive Terminal Menu Interface
Author: Kartikeya Pradhan
Subject: Python Programming (Semester 3)

This module provides the terminal-based interactive user interface for
the RetailPulse application. It handles menu navigation, formatted text-based
analytical summaries, data reload requests, error handling, and orchestrates
launching Matplotlib visualizations.
"""

from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple

from src.data_loader import load_sales_data
from src.data_processor import (
    calculate_kpis,
    get_branch_sales,
    get_category_gross_income,
    get_category_sales,
    get_customer_type_distribution,
    get_monthly_sales,
    get_payment_distribution,
    get_rating_analysis,
)
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


SEPARATOR = "=" * 80
THIN_SEPARATOR = "-" * 80


def display_banner() -> None:
    """Print the formatted RetailPulse ASCII art header and metadata."""
    print("\n" + SEPARATOR)
    print(r"""
  ██████╗ ███████╗████████╗ █████╗ ██╗██╗     ██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║     ██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ██████╔╝█████╗     ██║   ███████║██║██║     ██████╔╝██║   ██║██║     ███████╗█████╗  
  ██╔══██╗██╔══╝     ██║   ██╔══██║██║██║     ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  
  ██║  ██║███████╗   ██║   ██║  ██║██║███████╗██║     ╚██████╔╝███████╗███████║███████╗
  ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
    """)
    print("                RETAIL SALES ANALYTICS & EXECUTIVE DASHBOARD")
    print("                 Academic Mini-Project | Python Programming")
    print(SEPARATOR)


def display_dataset_info(records: List[Dict[str, Any]], filepath: Path | str) -> None:
    """Print a concise summary of the currently loaded dataset."""
    path_obj = Path(filepath)
    kpis = calculate_kpis(records)
    print(f"\n[+] Active Dataset : {path_obj.name} ({path_obj.resolve()})")
    print(f"[+] Total Records  : {kpis['total_transactions']:,} verified transactions")
    print(f"[+] Total Revenue  : ${kpis['total_revenue']:,.2f}")
    print(f"[+] Total Quantity : {kpis['total_units_sold']:,} units sold")
    print(f"[+] Average Order  : ${kpis['average_order_value']:,.2f}")
    print(f"[+] Overall Rating : {kpis['average_rating']:.2f} ★")
    print(THIN_SEPARATOR)


def display_menu_options() -> None:
    """Display the 10 numbered primary menu options."""
    print("\nSelect an analytical module or visualization action:")
    print("  [1]  View Complete Visual Dashboard     (Multi-Chart Master Window)")
    print("  [2]  Monthly Revenue Analysis           (Chronological Trend & Table)")
    print("  [3]  Product Category Analysis          (Sales & Volume by Category)")
    print("  [4]  Branch Performance                 (Revenue, Orders & Branch Metrics)")
    print("  [5]  Payment Method Analysis            (Ewallet, Cash, Credit Card Shares)")
    print("  [6]  Customer Type Analysis             (Member vs Normal Shopper Breakdown)")
    print("  [7]  Gross Income Analysis              (Profit Contribution by Category)")
    print("  [8]  Customer Rating Analysis           (Satisfaction Ratings by Category)")
    print("  [9]  Reload Dataset                     (Refresh from Disk / Switch Path)")
    print("  [10] Exit Application")
    print(SEPARATOR)


# -----------------------------------------------------------------------------
# Formatted Analytical Tables
# -----------------------------------------------------------------------------

def show_kpi_summary_table(records: List[Dict[str, Any]]) -> None:
    """Print the complete executive KPI metrics summary."""
    kpis = calculate_kpis(records)
    print("\n" + THIN_SEPARATOR)
    print("                EXECUTIVE KEY PERFORMANCE INDICATORS (KPIs)")
    print(THIN_SEPARATOR)
    print(f"  • Total Gross Revenue          : ${kpis['total_revenue']:,.2f}")
    print(f"  • Total Valid Transactions     : {kpis['total_transactions']:,}")
    print(f"  • Total Product Units Sold     : {kpis['total_units_sold']:,} units")
    print(f"  • Average Order Value (AOV)    : ${kpis['average_order_value']:,.2f}")
    print(f"  • Total Gross Income (Profit)  : ${kpis['total_gross_income']:,.2f}")
    print(f"  • Average Customer Rating      : {kpis['average_rating']:.2f} / 10.0 ★")
    print(THIN_SEPARATOR)


def show_monthly_sales_table(records: List[Dict[str, Any]]) -> None:
    """Print formatted chronological monthly performance table."""
    monthly = get_monthly_sales(records)
    total_rev = sum(m["revenue"] for m in monthly.values())

    print("\n" + THIN_SEPARATOR)
    print("                     MONTHLY SALES PERFORMANCE TABLE")
    print(THIN_SEPARATOR)
    print(f"{'Month':<12} {'Revenue ($)':>16} {'% Share':>10} {'Orders':>10} {'Units Sold':>12}")
    print("-" * 64)

    for ym, data in monthly.items():
        rev = data["revenue"]
        pct = (rev / total_rev * 100) if total_rev > 0 else 0.0
        orders = data["transactions"]
        units = data["units_sold"]
        print(f"{data['label']:<12} {f'${rev:,.2f}':>16} {f'{pct:.1f}%':>10} {orders:>10} {units:>12}")

    print("-" * 64)
    print(f"{'Total':<12} {f'${total_rev:,.2f}':>16} {'100.0%':>10} {len(records):>10} {sum(r['Quantity'] for r in records):>12}")
    print(THIN_SEPARATOR)


def show_category_sales_table(records: List[Dict[str, Any]]) -> None:
    """Print formatted category sales rankings table."""
    cat_sales = get_category_sales(records, sort_descending=True)
    cat_income = get_category_gross_income(records, sort_descending=False)
    total_rev = sum(cat_sales.values())

    print("\n" + THIN_SEPARATOR)
    print("                  PRODUCT CATEGORY REVENUE & PROFIT RANKING")
    print(THIN_SEPARATOR)
    print(f"{'Rank':<5} {'Product Line':<26} {'Revenue ($)':>15} {'% Share':>10} {'Gross Income':>14}")
    print("-" * 74)

    for rank, (cat, rev) in enumerate(cat_sales.items(), start=1):
        pct = (rev / total_rev * 100) if total_rev > 0 else 0.0
        income = cat_income.get(cat, 0.0)
        print(f"{rank:<5} {cat:<26} {f'${rev:,.2f}':>15} {f'{pct:.1f}%':>10} {f'${income:,.2f}':>14}")

    print("-" * 74)
    print(f"{'Total':<31} {f'${total_rev:,.2f}':>15} {'100.0%':>10} {f'${sum(cat_income.values()):,.2f}':>14}")
    print(THIN_SEPARATOR)


def show_branch_performance_table(records: List[Dict[str, Any]]) -> None:
    """Print formatted supermarket branch comparison table."""
    branches = get_branch_sales(records)
    total_rev = sum(b["revenue"] for b in branches.values())

    print("\n" + THIN_SEPARATOR)
    print("                     BRANCH PERFORMANCE COMPARISON")
    print(THIN_SEPARATOR)
    print(f"{'Branch':<12} {'City':<14} {'Revenue ($)':>14} {'% Share':>9} {'Orders':>8} {'AOV ($)':>10} {'Rating':>8}")
    print("-" * 79)

    for b, data in branches.items():
        rev = data["revenue"]
        pct = (rev / total_rev * 100) if total_rev > 0 else 0.0
        print(
            f"Branch {b:<5} {data['city']:<14} {f'${rev:,.2f}':>14} {f'{pct:.1f}%':>9} "
            f"{data['transactions']:>8} {f'${data["average_order_value"]:,.2f}':>10} {f'{data["average_rating"]:.2f} ★':>8}"
        )

    print("-" * 79)
    print(f"{'Total / Avg':<26} {f'${total_rev:,.2f}':>14} {'100.0%':>9} {len(records):>8} {f'${total_rev/len(records):,.2f}':>10} {'--':>8}")
    print(THIN_SEPARATOR)


def show_payment_table(records: List[Dict[str, Any]]) -> None:
    """Print formatted payment method distribution table."""
    payments = get_payment_distribution(records)

    print("\n" + THIN_SEPARATOR)
    print("                     PAYMENT METHOD BREAKDOWN")
    print(THIN_SEPARATOR)
    print(f"{'Payment Method':<18} {'Orders':>10} {'% Orders':>12} {'Revenue ($)':>16} {'% Revenue':>12}")
    print("-" * 72)

    for method, data in payments.items():
        cnt = data["count"]
        pct_c = data["percentage_count"]
        rev = data["revenue"]
        pct_r = data["percentage_revenue"]
        print(f"{method:<18} {cnt:>10} {f'{pct_c:.1f}%':>12} {f'${rev:,.2f}':>16} {f'{pct_r:.1f}%':>12}")

    print("-" * 72)
    tot_cnt = sum(p["count"] for p in payments.values())
    tot_rev = sum(p["revenue"] for p in payments.values())
    print(f"{'Total':<18} {tot_cnt:>10} {'100.0%':>12} {f'${tot_rev:,.2f}':>16} {'100.0%':>12}")
    print(THIN_SEPARATOR)


def show_customer_table(records: List[Dict[str, Any]]) -> None:
    """Print formatted Member vs Normal customer distribution table."""
    customers = get_customer_type_distribution(records)

    print("\n" + THIN_SEPARATOR)
    print("                     CUSTOMER TYPE SEGMENTATION")
    print(THIN_SEPARATOR)
    print(f"{'Customer Type':<18} {'Orders':>10} {'% Volume':>12} {'Revenue ($)':>16} {'% Revenue':>12}")
    print("-" * 72)

    for cust_type, data in customers.items():
        cnt = data["count"]
        pct_c = data["percentage_count"]
        rev = data["revenue"]
        pct_r = data["percentage_revenue"]
        print(f"{cust_type:<18} {cnt:>10} {f'{pct_c:.1f}%':>12} {f'${rev:,.2f}':>16} {f'{pct_r:.1f}%':>12}")

    print("-" * 72)
    tot_cnt = sum(c["count"] for c in customers.values())
    tot_rev = sum(c["revenue"] for c in customers.values())
    print(f"{'Total':<18} {tot_cnt:>10} {'100.0%':>12} {f'${tot_rev:,.2f}':>16} {'100.0%':>12}")
    print(THIN_SEPARATOR)


def show_gross_income_table(records: List[Dict[str, Any]]) -> None:
    """Print formatted gross income / profit table."""
    cat_income = get_category_gross_income(records, sort_descending=True)
    total_income = sum(cat_income.values())

    print("\n" + THIN_SEPARATOR)
    print("                   GROSS INCOME (PROFIT) BY CATEGORY")
    print(THIN_SEPARATOR)
    print(f"{'Rank':<5} {'Product Line':<28} {'Gross Income ($)':>18} {'% Profit Share':>16}")
    print("-" * 71)

    for rank, (cat, inc) in enumerate(cat_income.items(), start=1):
        pct = (inc / total_income * 100) if total_income > 0 else 0.0
        print(f"{rank:<5} {cat:<28} {f'${inc:,.2f}':>18} {f'{pct:.1f}%':>16}")

    print("-" * 71)
    print(f"{'Total':<33} {f'${total_income:,.2f}':>18} {'100.0%':>16}")
    print(THIN_SEPARATOR)


def show_rating_table(records: List[Dict[str, Any]]) -> None:
    """Print formatted customer satisfaction rating analysis table."""
    rating_data = get_rating_analysis(records)
    by_cat = rating_data.get("by_category", {})

    print("\n" + THIN_SEPARATOR)
    print("                 CUSTOMER SATISFACTION RATING ANALYSIS")
    print(THIN_SEPARATOR)
    print(f"Overall Benchmark Average: {rating_data.get('overall_average', 0.0):.2f} / 10.0 ★\n")
    print(f"{'Product Line':<26} {'Avg Rating':>12} {'Ratings Count':>15} {'Score Range':>16}")
    print("-" * 73)

    for cat, info in by_cat.items():
        avg = info["average_rating"]
        cnt = info["count"]
        rng = f"[{info['min_rating']:.1f} - {info['max_rating']:.1f}]"
        print(f"{cat:<26} {f'{avg:.2f} ★':>12} {cnt:>15} {rng:>16}")

    print("-" * 73)
    print(THIN_SEPARATOR)


# -----------------------------------------------------------------------------
# Action Handler
# -----------------------------------------------------------------------------

def pause_for_user() -> None:
    """Prompt the user before returning to the main menu."""
    try:
        input("\nPress [Enter] to return to the main menu...")
    except (KeyboardInterrupt, EOFError):
        print()


def execute_menu_choice(
    choice: int,
    records: List[Dict[str, Any]],
    current_filepath: Path,
) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[Path]]:
    """
    Execute the selected menu action.

    Args:
        choice: Integer option (1-10).
        records: Currently loaded dataset records.
        current_filepath: Path to currently active dataset.

    Returns:
        Tuple[bool, Optional[records], Optional[filepath]]:
            - keep_running (bool): False if user chose Exit (10), True otherwise.
            - updated_records: New records if reloaded, else None.
            - updated_filepath: New filepath if reloaded, else None.
    """
    if choice == 1:
        # 1. Complete Dashboard
        print("\n[*] Generating complete RetailPulse executive dashboard...")
        show_kpi_summary_table(records)
        print("\n[+] Opening master dashboard in a separate window.")
        print("[+] Close the dashboard window to return to the menu.")
        render_complete_dashboard(records, show=True)
        print("[✓] Dashboard closed.")
        pause_for_user()
        return True, None, None

    elif choice == 2:
        # 2. Monthly Revenue Analysis
        print("\n[*] Processing monthly sales trends...")
        show_monthly_sales_table(records)
        print("\n[+] Opening monthly revenue trend line chart...")
        plot_monthly_revenue_trend(records, show=True)
        print("[✓] Chart closed.")
        pause_for_user()
        return True, None, None

    elif choice == 3:
        # 3. Product Category Analysis
        print("\n[*] Processing product category sales rankings...")
        show_category_sales_table(records)
        print("\n[+] Opening category revenue horizontal bar chart...")
        plot_revenue_by_category(records, show=True)
        print("[✓] Chart closed.")
        pause_for_user()
        return True, None, None

    elif choice == 4:
        # 4. Branch Performance
        print("\n[*] Processing supermarket branch metrics...")
        show_branch_performance_table(records)
        print("\n[+] Opening branch performance comparative bar chart...")
        plot_branch_performance(records, show=True)
        print("[✓] Chart closed.")
        pause_for_user()
        return True, None, None

    elif choice == 5:
        # 5. Payment Method Analysis
        print("\n[*] Processing payment method distribution...")
        show_payment_table(records)
        print("\n[+] Opening payment distribution donut chart...")
        plot_payment_distribution(records, show=True)
        print("[✓] Chart closed.")
        pause_for_user()
        return True, None, None

    elif choice == 6:
        # 6. Customer Type Analysis
        print("\n[*] Processing customer segmentation metrics...")
        show_customer_table(records)
        print("\n[+] Opening customer segmentation donut chart...")
        plot_customer_type_distribution(records, show=True)
        print("[✓] Chart closed.")
        pause_for_user()
        return True, None, None

    elif choice == 7:
        # 7. Gross Income Analysis
        print("\n[*] Processing gross profit contribution by category...")
        show_gross_income_table(records)
        print("\n[+] Opening gross income bar chart...")
        plot_gross_income_by_category(records, show=True)
        print("[✓] Chart closed.")
        pause_for_user()
        return True, None, None

    elif choice == 8:
        # 8. Customer Rating Analysis
        print("\n[*] Processing customer satisfaction scores...")
        show_rating_table(records)
        print("\n[+] Opening customer rating breakdown chart...")
        plot_rating_analysis(records, show=True)
        print("[✓] Chart closed.")
        pause_for_user()
        return True, None, None

    elif choice == 9:
        # 9. Reload Dataset
        print("\n" + THIN_SEPARATOR)
        print("                         RELOAD DATASET")
        print(THIN_SEPARATOR)
        print(f"Current file: {current_filepath.resolve()}")
        try:
            user_input = input(
                "Press [Enter] to reload current file, or enter new CSV path: "
            ).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Reload cancelled.")
            pause_for_user()
            return True, None, None

        target_path = Path(user_input) if user_input else current_filepath

        try:
            print(f"[*] Reloading and re-validating dataset from: {target_path}...")
            reloaded_records, report = load_sales_data(target_path, strict=False)
            print(f"[✓] Reload successful!")
            print(f"    • Total valid records: {report['valid_records']:,}")
            print(f"    • Invalid records    : {report['invalid_records']}")
            if report["warnings"]:
                print(f"    • Warnings: {len(report['warnings'])}")
            pause_for_user()
            return True, reloaded_records, target_path
        except Exception as err:
            print(f"[!] Reload failed: {err}")
            pause_for_user()
            return True, None, None

    elif choice == 10:
        # 10. Exit
        print("\n" + SEPARATOR)
        print("          Thank you for using RetailPulse. Have a great day!")
        print(SEPARATOR + "\n")
        return False, None, None

    return True, None, None


# -----------------------------------------------------------------------------
# Main Interactive Loop
# -----------------------------------------------------------------------------

def run_terminal_menu(initial_filepath: Path | str = "dataset/supermarket_sales.csv") -> None:
    """
    Launch the interactive RetailPulse terminal command center.

    Args:
        initial_filepath: Path to the default CSV dataset.
    """
    filepath = Path(initial_filepath)

    # 1. Initial dataset loading loop (handles missing initial files gracefully)
    records: Optional[List[Dict[str, Any]]] = None

    while records is None:
        try:
            records, report = load_sales_data(filepath, strict=False)
        except (FileNotFoundError, ValueError) as err:
            display_banner()
            print(f"\n[!] Dataset error: {err}")
            print(f"    Target path: {filepath.resolve()}\n")
            try:
                user_path = input("Enter valid CSV path or 'q' to exit: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting RetailPulse.")
                sys.exit(0)

            if user_path.lower() in ("q", "quit", "exit"):
                print("\nExiting RetailPulse.")
                sys.exit(0)

            filepath = Path(user_path)

    # 2. Main interactive loop
    display_banner()

    while True:
        display_dataset_info(records, filepath)
        display_menu_options()

        try:
            raw_choice = input("Enter your choice [1-10]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] Interruption detected. Exiting RetailPulse. Goodbye!\n")
            break

        if not raw_choice:
            print("\n[!] Input cannot be empty. Please enter a number between 1 and 10.")
            continue

        try:
            choice = int(raw_choice)
        except ValueError:
            print(f"\n[!] Invalid input '{raw_choice}'. Please enter an integer from 1 to 10.")
            continue

        if not (1 <= choice <= 10):
            print(f"\n[!] Option {choice} is out of range. Please choose between 1 and 10.")
            continue

        keep_running, new_records, new_path = execute_menu_choice(choice, records, filepath)

        if not keep_running:
            break

        if new_records is not None and new_path is not None:
            records = new_records
            filepath = new_path

