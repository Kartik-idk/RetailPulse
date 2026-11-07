# RetailPulse 📊

> **Retail Sales Analytics Dashboard & Command Center**  
> *Subject:* Python Programming (Semester 3 Mini-Project)  
> *Developer:* Kartikeya Pradhan (Undergraduate Computer Science & Engineering)  
> *Platform:* macOS (Apple Silicon M4) | Python 3.14+  
> *GitHub Repository:* [https://github.com/Kartik-idk/RetailPulse](https://github.com/Kartik-idk/RetailPulse)

---

## 📌 Project Overview

**RetailPulse** is an academic retail sales analytics platform engineered to analyze supermarket transactional data using core Python programming concepts. It ingests historical supermarket sales records, cleans and validates each transaction, computes business Key Performance Indicators (KPIs), and delivers insights through two synchronized interfaces: an interactive terminal command center and an executive, dark-themed visual analytics dashboard powered by Matplotlib.

### Core Objectives
1. **Algorithmic Data Processing:** Ingest, clean, validate, and aggregate transactional records using Python's standard library (`csv`, `datetime`, `pathlib`, dictionaries, and lists) without depending on heavy third-party data science frameworks such as Pandas or NumPy.
2. **Interactive Terminal Command Center:** A fault-tolerant command-line interface providing structured text tables, formatted analytics, dataset reload capabilities, and menu-driven visualization routing.
3. **Executive Visual Dashboard:** A multi-chart dark-themed dashboard combining 5 KPI cards and 6 synchronized analytical charts inside a single Matplotlib window.

---

## 📊 Executive Visual Dashboard

The visualizer generates a high-resolution dark-themed analytics dashboard:

![RetailPulse Executive Dashboard Preview](dataset/dashboard_preview.png)

### Dashboard Layout Structure (`render_complete_dashboard`)
1. **Header Banner:** Application title in Electric Sky Blue (`#38BDF8`), dataset duration, and live transaction counter.
2. **KPI Banner (5 Custom `FancyBboxPatch` Cards):**
   - **Total Revenue:** `$322,966.75`
   - **Total Transactions:** `1,000`
   - **Total Units Sold:** `5,510`
   - **Average Order Value (AOV):** `$322.97`
   - **Average Customer Rating:** `6.97 ★`
3. **Subplot Grid (2 Rows × 3 Columns):**
   - **Monthly Revenue Trend:** Line chart with smooth fill area, markers, and values for Jan, Feb, and Mar 2019.
   - **Revenue by Product Category:** Horizontal bar chart sorted descending from Food & Beverages down to Health & Beauty.
   - **Payment Method Distribution:** Donut chart showing Ewallet (34.5%), Cash (34.4%), and Credit Card (31.1%) with center text and legend.
   - **Branch Performance:** Comparative bar chart for Branch Alex, Cairo, and Giza with transaction counts and ratings.
   - **Customer Type Distribution:** Donut chart comparing Member (56.5%) vs. Normal (43.5%) shopper volume and revenue share.
   - **Gross Income by Category:** Vertical bar chart comparing total gross profit by merchandise line.

---

## 🛠️ Technology Stack & Academic Constraints

- **Language:** Python 3 (Tested on Python 3.14.7)
- **Data Ingestion:** Standard library `csv` module (`csv.DictReader`)
- **Date & Time Processing:** Standard library `datetime`
- **Data Structures:** Native Python dictionaries, lists, sets, and tuples
- **Data Visualization:** `matplotlib` (Dark Navy `#0B1120` modern theme)
- **File System Management:** Standard library `pathlib`
- **Testing:** Standard library `unittest` and `unittest.mock`

### Strict Constraints
- ❌ **No Pandas:** All filtering, mapping, grouping, and aggregations are implemented with native Python loops and hash tables.
- ❌ **No External Processing Engines:** Preserves academic integrity and demonstrates mastery of foundational computational algorithms.
- ❌ **No Web Frameworks or Databases:** Standalone desktop CLI and native Matplotlib window interface.

---

## 🧠 Python Concepts Demonstrated

1. **File I/O & Streaming:** Robust file handling with context managers (`with open(...)`), UTF-8 BOM stripping (`utf-8-sig`), and streaming CSV rows via `csv.DictReader`.
2. **Dynamic Hash Tables (Dictionaries):** $O(N)$ linear-time aggregations using dictionaries as accumulators (`dict.get()`, `dict.items()`, and key-value mapping).
3. **List Comprehensions & Higher-Order Sorting:** Data transformation and multi-criteria sorting using `sorted()` with custom lambda functions.
4. **Data Validation & Type Casting:** Strict schema validation, value range assertions, date parsing (`strptime`), and error reporting.
5. **Defensive Programming & Exception Handling:** Structured handling of `FileNotFoundError`, `ValueError`, `KeyboardInterrupt`, and `EOFError`.
6. **Object-Oriented Graphical Canvas:** Utilizing Matplotlib's `Figure`, `Axes`, `GridSpec`, `ticker`, and `FancyBboxPatch` APIs.
7. **Automated Testing & Mocking:** Unit and integration testing using `unittest.TestCase`, test fixtures (`setUp`/`tearDown`), and function mocking via `unittest.mock.patch`.

---

## 📂 Project Architecture

```text
RetailPulse/
│
├── dataset/
│   ├── .gitkeep
│   ├── supermarket_sales.csv     # Historical supermarket sales dataset (1,000 records)
│   └── dashboard_preview.png     # Rendered executive dashboard preview image
│
├── docs/
│   ├── PROJECT_REPORT.md         # Comprehensive academic project report
│   ├── VIVA_PREPARATION.md       # 35 technical viva questions and detailed answers
│   └── USER_GUIDE.md             # Complete user and execution manual
│
├── src/
│   ├── __init__.py               # Package metadata and version info
│   ├── data_loader.py            # CSV reading, schema validation, type parsing
│   ├── data_processor.py         # Business logic, KPI calculations, aggregations
│   ├── visualizer.py             # Matplotlib dark-themed dashboard and subplots
│   └── terminal_menu.py          # Interactive command-line interface & text tables
│
├── tests/
│   ├── __init__.py
│   ├── test_data_processor.py    # Unit tests for loading and analytics (21 tests)
│   ├── test_visualizer.py        # Smoke tests for Matplotlib plotting (9 tests)
│   └── test_terminal_menu.py     # Integration tests for menu & routing (22 tests)
│
├── main.py                       # Application entry point
├── requirements.txt              # External dependencies (matplotlib>=3.8.0)
├── README.md                     # Comprehensive project documentation
├── .gitignore                    # Git ignore specifications
└── .venv/                        # Isolated Python virtual environment
```

---

## 📈 Dataset Specifications

The application utilizes the historical **Supermarket Sales** dataset.

- **Source:** [Kaggle - Supermarket Sales (Fares Ashraf)](https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales)
- **License:** Apache 2.0 (Permits open redistribution and academic use)
- **File Location:** `dataset/supermarket_sales.csv`
- **File Size:** 140,285 bytes (~137 KB)
- **Records:** 1,000 transactions (0 duplicates, 0 missing values)
- **Time Horizon:** January 1, 2019 – March 30, 2019

### Verified Column Schema (17 Columns)

| # | Column Name | Python Type | Description / Sample Value |
|---|---|---|---|
| 0 | `Invoice ID` | `str` | Unique transaction invoice identifier (e.g., `750-67-8428`) |
| 1 | `Branch` | `str` | Supermarket branch identifier (`Alex`, `Giza`, `Cairo`) |
| 2 | `City` | `str` | Location of branch (`Yangon`, `Naypyitaw`, `Mandalay`) |
| 3 | `Customer type` | `str` | Customer category (`Member`, `Normal`) |
| 4 | `Gender` | `str` | Customer gender (`Female`, `Male`) |
| 5 | `Product line` | `str` | Merchandise category (6 distinct lines) |
| 6 | `Unit price` | `float` | Price per item in USD ($10.08 – $99.96) |
| 7 | `Quantity` | `int` | Units purchased per transaction (1 – 10) |
| 8 | `Tax 5%` | `float` | 5% customer tax fee applied to purchase |
| 9 | `Sales` | `float` | **Total Invoice Revenue** ($10.68 – $1,042.65) |
| 10 | `Date` | `datetime.date` | Transaction date (`%m/%d/%Y`, e.g., `1/5/2019`) |
| 11 | `Time` | `str` | Operating hours timestamp (10:00 AM – 9:00 PM) |
| 12 | `Payment` | `str` | Payment method (`Ewallet`, `Cash`, `Credit card`) |
| 13 | `cogs` | `float` | Cost of goods sold ($10.17 – $993.00) |
| 14 | `gross margin percentage` | `float` | Profit margin percentage (fixed at `4.761904762%`) |
| 15 | `gross income` | `float` | Gross profit per transaction ($0.51 – $49.65) |
| 16 | `Rating` | `float` | Customer satisfaction rating (4.0 – 10.0 scale) |

---

## 💻 Terminal Menu Walkthrough

Launch the application to access the 10-option interactive menu:

```text
================================================================================
  ██████╗ ███████╗████████╗ █████╗ ██╗██╗     ██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║     ██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ██████╔╝█████╗     ██║   ███████║██║██║     ██████╔╝██║   ██║██║     ███████╗█████╗  
  ██╔══██╗██╔══╝     ██║   ██╔══██║██║██║     ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  
  ██║  ██║███████╗   ██║   ██║  ██║██║███████╗██║     ╚██████╔╝███████╗███████║███████╗
  ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
                RETAIL SALES ANALYTICS & EXECUTIVE DASHBOARD
================================================================================

[+] Active Dataset : supermarket_sales.csv
[+] Total Records  : 1,000 verified transactions
[+] Total Revenue  : $322,966.75
[+] Total Quantity : 5,510 units sold
[+] Average Order  : $322.97
[+] Overall Rating : 6.97 ★
--------------------------------------------------------------------------------

Select an analytical module or visualization action:
  [1]  View Complete Visual Dashboard     (Multi-Chart Master Window)
  [2]  Monthly Revenue Analysis           (Chronological Trend & Table)
  [3]  Product Category Analysis          (Sales & Volume by Category)
  [4]  Branch Performance                 (Revenue, Orders & Branch Metrics)
  [5]  Payment Method Analysis            (Ewallet, Cash, Credit Card Shares)
  [6]  Customer Type Analysis             (Member vs Normal Shopper Breakdown)
  [7]  Gross Income Analysis              (Profit Contribution by Category)
  [8]  Customer Rating Analysis           (Satisfaction Ratings by Category)
  [9]  Reload Dataset                     (Refresh from Disk / Switch Path)
  [10] Exit Application
================================================================================
```

| Option | Function | Description |
|---|---|---|
| **1** | Complete Dashboard | Displays terminal KPI cards and launches the master 2×3 Matplotlib window |
| **2** | Monthly Trends | Prints monthly revenue table and opens the line chart trend view |
| **3** | Category Sales | Prints revenue and % share per merchandise line and opens horizontal bar chart |
| **4** | Branch Performance | Prints comparison table (Alex, Cairo, Giza) and opens branch performance bar chart |
| **5** | Payment Analysis | Prints volume/revenue breakdown and opens payment method donut chart |
| **6** | Customer Analysis | Prints Member vs Normal customer metrics and opens customer donut chart |
| **7** | Gross Income | Prints profit contribution table and opens gross income bar chart |
| **8** | Rating Analysis | Prints category-level satisfaction scores and opens rating comparison chart |
| **9** | Reload Dataset | Refreshes the CSV from disk, re-validates, and recalculates all metrics in-memory |
| **10** | Exit | Cleanly terminates the application with a friendly farewell message |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher (Python 3.14 recommended)
- Git & GitHub CLI (`gh`)

### Installation & Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kartik-idk/RetailPulse.git
   cd RetailPulse
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Run with a custom dataset path:**
   ```bash
   python main.py path/to/custom_dataset.csv
   ```

6. **View command line help:**
   ```bash
   python main.py --help
   ```

---

## 🧪 Testing & Quality Assurance

The project includes an automated test suite containing **52 tests** built with Python's standard `unittest` framework:

```bash
# Run the complete test suite
python3 -m unittest discover -s tests -v
```

### Test Suite Structure (52 Tests)
- **`tests/test_data_processor.py` (21 tests):**
  - Header validation (missing, empty, valid headers).
  - Row validation (boundary checks, negative quantity, invalid ratings, corrupted dates).
  - Type conversion (int, float, datetime.date casting).
  - KPI calculations with controlled, deterministic sample data.
  - Direct unit testing of individual KPI functions and zero-division protection.
  - Multi-dimensional aggregations (monthly chronological ordering, category rankings, branch metrics, payment distributions, customer segmentation).
- **`tests/test_visualizer.py` (9 tests):**
  - Headless backend verification (`matplotlib.use("Agg")`).
  - Standalone chart generation for all 7 chart types.
  - Master dashboard GridSpec layout rendering (validates all 12 subplot axes).
  - Empty record list handling (graceful `"No Data Available"` placeholders).
- **`tests/test_terminal_menu.py` (22 tests):**
  - Text table formatting for all analytical views.
  - Menu option routing (options 1–8 with mocked visualizers).
  - Dataset reload functionality (re-reading from disk and error recovery on missing file).
  - Input validation (empty inputs, non-integer strings, out-of-range numbers).
  - Missing file startup recovery and exit logic.

---

## ⚠️ Limitations

1. **Dataset Horizon:** The dataset covers transactions from January 1, 2019 to March 30, 2019 (3 months). Annual or multi-year seasonality trends cannot be inferred without additional historical data.
2. **Granular SKU Data:** Individual item names/SKUs are not present in the dataset; product analysis is performed at the *Product line* category level.
3. **Display Server Dependency for GUI:** Viewing Matplotlib charts requires an active graphical window manager (e.g. macOS Quartz, Windows GUI, or X11/Wayland). Headless environments can execute all text summaries and export charts to disk.

---

## 🔮 Future Improvements

1. **Multi-File Batch Merging:** Supporting directory scanning to merge quarterly sales files across multiple years.
2. **PDF Briefing Export:** Implementing one-click multi-page executive PDF report generation via `matplotlib.backends.backend_pdf.PdfPages`.
3. **RFM Segmentation Engine:** Implementing Recency, Frequency, and Monetary customer segmentation algorithms using core Python.
4. **Statistical Forecasting:** Trend extrapolation for future quarterly inventory planning using standard library mathematical functions.

---

## 📚 Project Documentation Links

- 📄 [Comprehensive Academic Project Report](docs/PROJECT_REPORT.md)
- 🎓 [35-Question Python Viva Voce Preparation Guide](docs/VIVA_PREPARATION.md)
- 📖 [Complete User Manual & Execution Guide](docs/USER_GUIDE.md)

---

## 👨‍💻 Author & Academic Information

- **Developer:** Kartikeya Pradhan
- **Subject:** Python Programming (Semester 3)
- **Degree:** B.Tech in Computer Science & Engineering
- **Institution:** Individual Academic Submission

---

## 📋 Development Roadmap

- [x] **Milestone 1:** Workspace and GitHub Initialization
- [x] **Milestone 2:** Dataset Acquisition & Verification
- [x] **Milestone 3:** Core Data Loading & Processing Modules
- [x] **Milestone 4:** Matplotlib Visualizations & Dashboard Layout
- [x] **Milestone 5:** Terminal Interface Integration
- [x] **Milestone 6:** Final Testing, Verification, and Documentation
