"""
RetailPulse - Retail Sales Analytics Dashboard
Main Application Entry Point
Author: Kartikeya Pradhan
Subject: Python Programming (Semester 3)

This script serves as the primary entry point for the RetailPulse application.
It determines the project root, resolves the dataset location, and launches
the interactive terminal menu interface.

Usage:
    python main.py
    python main.py [optional_path_to_dataset.csv]
"""

from pathlib import Path
import sys

# Ensure the project root directory is on the Python module search path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.terminal_menu import run_terminal_menu


def main() -> None:
    """Resolve dataset path and launch the interactive terminal menu."""
    default_dataset = PROJECT_ROOT / "dataset" / "supermarket_sales.csv"

    # Support optional command line argument for custom dataset path
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        if arg in ("--help", "-h"):
            print("RetailPulse - Retail Sales Analytics Dashboard")
            print("\nUsage:")
            print("  python main.py                     Launch with default dataset")
            print("  python main.py <path_to_csv>       Launch with a specified CSV file")
            print("  python main.py --help              Show this help message")
            sys.exit(0)
        dataset_path = Path(arg)
    else:
        dataset_path = default_dataset

    run_terminal_menu(dataset_path)


if __name__ == "__main__":
    main()
