"""
RetailPulse - Data Loader Module
Author: Kartikeya Pradhan
Subject: Python Programming (Semester 3)

This module handles reading, validating, and type-converting transactional
data from the Supermarket Sales CSV file using Python's standard library
`csv`, `datetime`, and `pathlib` modules.
No third-party data processing libraries (e.g. Pandas, NumPy) are used.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Verified column names expected in the Supermarket Sales dataset.
VERIFIED_COLUMNS = [
    "Invoice ID",
    "Branch",
    "City",
    "Customer type",
    "Gender",
    "Product line",
    "Unit price",
    "Quantity",
    "Tax 5%",
    "Sales",
    "Date",
    "Time",
    "Payment",
    "cogs",
    "gross margin percentage",
    "gross income",
    "Rating",
]

# Standard date format verified in dataset (%m/%d/%Y e.g. '1/5/2019')
PRIMARY_DATE_FORMAT = "%m/%d/%Y"


def validate_headers(headers: List[str]) -> bool:
    """
    Validate that all required columns are present in the CSV header row.
    Header names are stripped of whitespace before comparison.

    Args:
        headers: List of raw column names from the CSV file.

    Returns:
        bool: True if all verified columns are present.

    Raises:
        ValueError: If headers are empty or missing any required columns.
    """
    if not headers:
        raise ValueError("CSV file has no header row or is empty.")

    cleaned_headers = [h.strip() for h in headers if h is not None]
    missing = [col for col in VERIFIED_COLUMNS if col not in cleaned_headers]

    if missing:
        raise ValueError(
            f"CSV file is missing {len(missing)} required column(s): {missing}. "
            f"Found columns: {cleaned_headers}"
        )

    return True


def validate_record(record: Dict[str, Any]) -> bool:
    """
    Validate whether a single CSV record contains all required fields and valid data.

    Args:
        record: Dictionary representing a raw or partially processed CSV row.

    Returns:
        bool: True if the record meets all validation rules.

    Raises:
        ValueError: With a detailed description if any validation rule is violated.
    """
    # Check essential string fields are non-empty
    for field in ("Invoice ID", "Branch", "Product line", "Date", "Sales"):
        val = str(record.get(field, "")).strip()
        if not val:
            raise ValueError(f"Field '{field}' cannot be empty.")

    # Validate date parsing
    raw_date = str(record.get("Date", "")).strip()
    try:
        datetime.strptime(raw_date, PRIMARY_DATE_FORMAT)
    except ValueError:
        # Fallback check for alternative ISO format
        try:
            datetime.strptime(raw_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"Invalid date format '{raw_date}'. Expected '{PRIMARY_DATE_FORMAT}'."
            )

    # Validate numerical conversions and positive bounds
    try:
        unit_price = float(record.get("Unit price", ""))
        quantity = int(record.get("Quantity", ""))
        tax = float(record.get("Tax 5%", ""))
        sales = float(record.get("Sales", ""))
        cogs = float(record.get("cogs", ""))
        margin_pct = float(record.get("gross margin percentage", ""))
        gross_income = float(record.get("gross income", ""))
        rating = float(record.get("Rating", ""))
    except (ValueError, TypeError) as err:
        raise ValueError(f"Numerical conversion error: {err}")

    if unit_price < 0 or quantity <= 0 or sales < 0 or cogs < 0 or gross_income < 0:
        raise ValueError(f"Numerical values must be non-negative (quantity must be > 0).")

    if not (0.0 <= rating <= 10.0):
        raise ValueError(f"Rating {rating} is out of acceptable bounds [0.0, 10.0].")

    return True


def convert_record_types(record: Dict[str, str]) -> Dict[str, Any]:
    """
    Convert raw string fields in a validated CSV row into appropriate Python data types.

    Conversions:
        - Quantity -> int
        - Unit price, Tax 5%, Sales, cogs, gross margin percentage, gross income, Rating -> float
        - Date -> datetime.date
        - Time, Branch, City, Product line, Customer type, Gender, Payment -> stripped str

    Args:
        record: Raw string dictionary from csv.DictReader.

    Returns:
        Dict[str, Any]: Strongly typed dictionary ready for processing.
    """
    raw_date = record["Date"].strip()
    try:
        parsed_dt = datetime.strptime(raw_date, PRIMARY_DATE_FORMAT)
    except ValueError:
        parsed_dt = datetime.strptime(raw_date, "%Y-%m-%d")

    sales = float(record["Sales"].strip())

    return {
        "Invoice ID": record["Invoice ID"].strip(),
        "Branch": record["Branch"].strip(),
        "City": record.get("City", "").strip(),
        "Customer type": record.get("Customer type", "").strip(),
        "Gender": record.get("Gender", "").strip(),
        "Product line": record["Product line"].strip(),
        "Unit price": float(record["Unit price"].strip()),
        "Quantity": int(record["Quantity"].strip()),
        "Tax 5%": float(record["Tax 5%"].strip()),
        "Sales": sales,
        "Date": parsed_dt.date(),
        "Date_str": raw_date,
        "YearMonth": parsed_dt.strftime("%Y-%m"),
        "MonthName": parsed_dt.strftime("%b %Y"),
        "Time": record.get("Time", "").strip(),
        "Payment": record.get("Payment", "").strip(),
        "cogs": float(record["cogs"].strip()),
        "gross margin percentage": float(record["gross margin percentage"].strip()),
        "gross income": float(record["gross income"].strip()),
        "Rating": float(record["Rating"].strip()),
    }


def load_sales_data(
    filepath: Path | str,
    strict: bool = False,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Load, validate, and parse transactional sales data from a CSV file.

    Args:
        filepath: Absolute or relative path to the CSV file.
        strict: If True, halts immediately on any invalid row.
                If False, logs invalid rows to the report and continues.

    Returns:
        Tuple[List[Dict[str, Any]], Dict[str, Any]]:
            - records: List of validated and typed transaction dictionaries.
            - report: Processing metadata containing total rows, valid counts,
                      invalid counts, and warning messages.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If file is not a file, is empty, or lacks required headers.
    """
    path = Path(filepath)

    # 1. Verify file existence
    if not path.exists():
        raise FileNotFoundError(f"Dataset file does not exist: {path.resolve()}")

    if not path.is_file():
        raise ValueError(f"Specified path is a directory, not a file: {path.resolve()}")

    records: List[Dict[str, Any]] = []
    warnings: List[str] = []
    total_raw_rows = 0

    # 2. Read CSV without modifying original content
    with open(path, mode="r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        # 3. Validate header row
        if reader.fieldnames is None:
            raise ValueError(f"CSV file is empty: {path.resolve()}")

        validate_headers(list(reader.fieldnames))

        # 4. Iterate and process each row
        for row_index, raw_row in enumerate(reader, start=1):
            total_raw_rows += 1
            # Normalize keys by stripping whitespace
            cleaned_row = {
                (k.strip() if k else ""): (v.strip() if v else "")
                for k, v in raw_row.items()
            }

            try:
                validate_record(cleaned_row)
                typed_record = convert_record_types(cleaned_row)
                records.append(typed_record)
            except ValueError as err:
                msg = f"Row {row_index} (Invoice: {cleaned_row.get('Invoice ID', 'N/A')}): {err}"
                if strict:
                    raise ValueError(msg) from err
                warnings.append(msg)

    if total_raw_rows == 0:
        raise ValueError(f"Dataset at {path.resolve()} contains header only with 0 data rows.")

    report = {
        "file_path": str(path.resolve()),
        "total_raw_rows": total_raw_rows,
        "valid_records": len(records),
        "invalid_records": len(warnings),
        "warnings": warnings,
    }

    return records, report
