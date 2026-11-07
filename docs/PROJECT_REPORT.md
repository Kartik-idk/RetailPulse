# RetailPulse: Retail Sales Analytics Dashboard
## Academic Project Report

**Subject:** Python Programming (Semester 3)  
**Degree:** Bachelor of Technology in Computer Science & Engineering  
**Student Name:** Kartikeya Pradhan  
**System Architecture:** Modular Standalone Application  
**Development Platform:** macOS (Apple Silicon M4) | Python 3.14  
**Source Repository:** [https://github.com/Kartik-idk/RetailPulse](https://github.com/Kartik-idk/RetailPulse)

---

## 1. Introduction

Retail analytics is a critical domain in enterprise data science, allowing supermarket managers and commercial analysts to uncover transactional patterns, monitor customer preferences, and evaluate revenue trends. With the advent of large transactional datasets, modern computing demands robust systems capable of extracting meaningful business intelligence from raw data.

**RetailPulse** is an academic retail sales analytics platform engineered to demonstrate core computational thinking and software engineering principles in Python. The system reads historical supermarket transactional records from a flat CSV file, validates and cleans individual transaction attributes, performs multi-dimensional aggregations, and surfaces insights through two synchronized interfaces: an interactive command-line interface (CLI) and an executive, dark-themed visual analytics dashboard generated using Matplotlib.

---

## 2. Problem Statement

Many contemporary data science applications rely on monolithic, third-party libraries (such as Pandas, Polars, or NumPy) or heavyweight web micro-frameworks (such as Flask, Django, or Streamlit). While suitable for production systems, relying heavily on high-level libraries in an academic context often abstracts away fundamental algorithmic concepts, such as:
- Linear file parsing and buffer management.
- Dynamic key-value hash map aggregations.
- Exception propagation and input validation.
- Object-oriented graphical canvas manipulation.

The objective of this project is to build an end-to-end, fault-tolerant analytics system that achieves production-grade visual polish and data integrity using **Python's standard library** (`csv`, `datetime`, `pathlib`) for all business logic and **Matplotlib** for data visualization.

---

## 3. Project Objectives

1. **Robust Ingestion & Schema Validation:** Implement a CSV ingestion pipeline using `csv.DictReader` that validates headers, verifies positive value ranges, enforces valid date formats, and gracefully isolates corrupted rows.
2. **Core Python Aggregations:** Design reusable business logic functions that calculate key performance indicators (Total Revenue, Transactions, Units Sold, Average Order Value, Customer Rating, Gross Profit) and multi-dimensional aggregations without Pandas.
3. **Executive Visual Analytics:** Build a synchronized dark-themed dashboard using Matplotlib's object-oriented `GridSpec` layout, presenting 5 KPI metric cards and 6 complementary charts.
4. **Interactive Command-Line Application:** Develop an intuitive, menu-driven terminal interface featuring formatted ASCII tables, user input validation, dynamic dataset reloading, and clean exception handling.
5. **Quality Assurance & Verification:** Establish an automated test suite using `unittest` covering edge cases, empty datasets, and GUI mocking.

---

## 4. Tools & Technologies

| Component | Technology | Rationale & Academic Significance |
|---|---|---|
| **Programming Language** | Python 3.14+ | High readability, rich standard library, and strong support for object-oriented and modular programming. |
| **Data Ingestion** | Standard `csv` (`DictReader`) | Streams tabular data as ordered key-value mappings without third-party dependencies. |
| **Date & Time Processing** | Standard `datetime` | Facilitates strict date parsing (`%m/%d/%Y`), chronological sorting, and Year-Month grouping. |
| **Data Aggregation** | Native Dictionaries & Lists | Achieves $O(N)$ linear time complexity for grouping and accumulative calculations using hash maps. |
| **File Management** | Standard `pathlib.Path` | Platform-independent path resolution across macOS, Linux, and Windows. |
| **Visualization Engine** | `matplotlib` (pyplot & gridspec) | Complete control over visual styling, axes, canvas patches, layout spacing, and custom color themes. |
| **Test Suite** | Standard `unittest` & `mock` | Automated unit testing and integration testing with headless non-interactive backends. |
| **Version Control** | Git & GitHub | Professional versioning, milestone-based commit history, and remote tracking. |

---

## 5. System Architecture

The RetailPulse system adheres to the **Separation of Concerns (SoC)** principle, isolating file I/O, business logic computation, terminal user interaction, and graphical rendering into distinct modules:

```text
                           ┌────────────────────────┐
                           │      User Terminal     │
                           └───────────┬────────────┘
                                       │
                                       ▼
                             ┌───────────────────┐
                             │      main.py      │
                             │ (Entry Controller)│
                             └─────────┬─────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        ┌───────────────────────┐             ┌───────────────────────┐
        │   src/data_loader.py  │             │ src/terminal_menu.py  │
        │(CSV Streaming & Valid)│             │ (CLI & Text Summary)  │
        └───────────┬───────────┘             └───────────┬───────────┘
                    │                                     │
                    ▼                                     │
        ┌───────────────────────┐                         │
        │ src/data_processor.py │◄────────────────────────┘
        │(KPIs & Aggregations)  │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   src/visualizer.py   │
        │(Matplotlib Dashboard) │
        └───────────────────────┘
```

---

## 6. Module Descriptions

### 6.1 `src/data_loader.py`
Responsible for reading raw CSV transactional data from `dataset/supermarket_sales.csv`:
- `validate_headers(headers)`: Verifies that all 17 mandatory columns are present in the header row, raising a informative `ValueError` if columns are missing.
- `validate_record(record)`: Validates individual records to ensure non-empty identifiers, parseable date formats, positive numerical bounds (e.g. quantity $> 0$, unit price $\ge 0$), and valid rating scales ($0.0 \le \text{rating} \le 10.0$).
- `convert_record_types(record)`: Casts string records into strongly-typed primitives (`int`, `float`, and `datetime.date`), extracting derived fields like `YearMonth` and `MonthName`.
- `load_sales_data(filepath, strict=False)`: Manages file opening with UTF-8 encoding, isolates corrupted records into a diagnostic report, and returns clean in-memory records.

### 6.2 `src/data_processor.py`
Implements core business intelligence aggregations using standard Python structures:
- `calculate_kpis(records)`: Computes Total Revenue, Total Transactions, Total Units Sold, Average Order Value (AOV), Average Rating, and Gross Income in a single pass.
- `get_category_sales(records)`: Groups revenue by merchandise product line, returning a dictionary sorted in descending order.
- `get_monthly_sales(records)`: Chronologically groups revenue, transaction counts, and unit volumes by `YYYY-MM`.
- `get_branch_sales(records)`: Computes branch-level metrics (Alex, Cairo, Giza) including revenue, volume, gross income, AOV, and customer satisfaction.
- `get_payment_distribution(records)`: Computes payment method shares (Ewallet, Cash, Credit Card) with count percentages and revenue percentages.
- `get_customer_type_distribution(records)`: Evaluates Member vs. Normal shopper volume and revenue contribution.
- `get_category_gross_income(records)`: Aggregates gross profit generated per product line.
- `get_rating_analysis(records)`: Evaluates overall and category-level average satisfaction scores and score ranges.

### 6.3 `src/visualizer.py`
Builds an executive dark-themed graphical dashboard using pure Matplotlib:
- Custom dark navy design system (`#0B1120` main canvas, `#151F32` panel cards, `#38BDF8` electric blue, `#A78BFA` purple, `#34D399` mint).
- 7 standalone chart functions (`plot_monthly_revenue_trend`, `plot_revenue_by_category`, `plot_branch_performance`, `plot_payment_distribution`, `plot_customer_type_distribution`, `plot_gross_income_by_category`, `plot_rating_analysis`).
- `render_complete_dashboard(records)`: Integrates all charts and 5 `FancyBboxPatch` KPI cards into a single high-resolution window via `matplotlib.gridspec.GridSpec`.

### 6.4 `src/terminal_menu.py`
Provides an interactive 10-option command center:
- Formatted text tables with clean column alignment.
- Menu routing connecting selections to visualizer plotting routines.
- In-memory dataset reload functionality that refreshes records from disk without restarting the process.
- Exception isolation preventing crashes on empty input, non-numeric strings, or `KeyboardInterrupt`.

### 6.5 `main.py`
Lightweight application bootstrapper:
- Automatically resolves absolute project root paths using `pathlib.Path(__file__).resolve().parent`.
- Supports CLI flags (`--help`, `-h`, or custom dataset paths).
- Launches the interactive terminal menu.

---

## 7. Algorithms & Mathematical Formulations

### 7.1 Key Performance Indicator Calculations
1. **Total Revenue:**
   $$\text{Total Revenue} = \sum_{i=1}^{N} \text{Sales}_i$$
2. **Average Order Value (AOV):**
   $$\text{AOV} = \frac{\text{Total Revenue}}{N} = \frac{\sum_{i=1}^{N} \text{Sales}_i}{N}$$
3. **Average Customer Rating:**
   $$\bar{R} = \frac{\sum_{i=1}^{N} \text{Rating}_i}{N}$$
4. **Total Gross Income:**
   $$\text{Gross Profit} = \sum_{i=1}^{N} \text{gross income}_i$$
   *(Verified: $\text{Unit Price} \times \text{Quantity} + \text{Tax 5\%} = \text{Sales}$)*

### 7.2 Chronological Monthly Aggregation
Monthly grouping employs dictionary hashing with ISO-8601 formatting keys (`YYYY-MM`):
```python
monthly_data = {}
for record in records:
    key = record["Date"].strftime("%Y-%m")
    if key not in monthly_data:
        monthly_data[key] = {"revenue": 0.0, "transactions": 0, "units_sold": 0}
    monthly_data[key]["revenue"] += record["Sales"]
    monthly_data[key]["transactions"] += 1
    monthly_data[key]["units_sold"] += record["Quantity"]
```
Because ISO date strings sort lexicographically identically to chronological time, calling `sorted(monthly_data.keys())` guarantees exact timeline ordering without sorting overhead.

---

## 8. Testing & Verification Results

The application includes an automated test suite containing **52 tests** across three test modules:

```text
----------------------------------------------------------------------
Ran 52 tests in 0.193s

OK
```

### Breakdown of Test Modules
- **`tests/test_data_processor.py` (21 tests):**
  - Schema and header verification.
  - Record data type conversion.
  - KPI calculation precision on controlled sample datasets.
  - Division-by-zero protection on empty datasets.
  - Aggregation logic verification for categories, months, branches, payments, and customers.
- **`tests/test_visualizer.py` (9 tests):**
  - Headless rendering verification under `matplotlib.use('Agg')`.
  - Verification that all 7 standalone chart functions produce valid `Figure` instances.
  - Verification that the master dashboard renders all 12 subplot axes without overlap.
  - Verification that empty datasets render clean `"No Data Available"` placeholders.
- **`tests/test_terminal_menu.py` (22 tests):**
  - Output table generation and column alignment.
  - Menu option routing (options 1 to 10).
  - In-memory dataset reload functionality.
  - Error recovery on non-existent dataset paths.
  - Input validation (handling non-numeric strings and out-of-bounds numbers).

### Integration Verification Against Real Dataset
Executed against `dataset/supermarket_sales.csv`:
- **Total Transactions:** 1,000 (Expected: 1,000) ✅
- **Total Revenue:** \$322,966.75 (Expected: \$322,966.75) ✅
- **Total Units Sold:** 5,510 (Expected: 5,510) ✅
- **Average Order Value:** \$322.97 (Expected: \$322.97) ✅
- **Total Gross Income:** \$15,379.37 (Expected: \$15,379.37) ✅
- **Average Customer Rating:** 6.97 ★ (Expected: 6.97 ★) ✅

---

## 9. Conclusion

RetailPulse successfully demonstrates that a complete, robust, and visually compelling data analytics platform can be built using core Python programming concepts and standard libraries. By eliminating dependence on Pandas and web frameworks, the codebase maintains full algorithmic transparency, minimal memory overhead, and straightforward maintainability suitable for undergraduate academic evaluation.

---

## 10. Future Scope

While RetailPulse fully satisfies all academic project criteria, potential future extensions could include:
1. **Multi-File Dataset Ingestion:** Ability to merge multiple quarterly CSV files into a multi-year comparative model.
2. **Automated PDF Report Export:** Using Matplotlib's `PdfPages` backend to compile executive analytics into downloadable PDF briefing packets.
3. **Advanced Customer RFM Segmentation:** Implementing Recency, Frequency, and Monetary (RFM) scoring using core Python algorithms.
4. **Forecasting Module:** Basic linear trend projection using standard library statistical algorithms.
