# RetailPulse: User Manual & Execution Guide

Welcome to the **RetailPulse User Guide**. This document provides step-by-step instructions for installing, configuring, running, and navigating the RetailPulse analytics system.

---

## 1. System Requirements

- **Operating System:** macOS (Apple Silicon or Intel), Linux, or Windows 10/11
- **Python:** Python 3.10 or higher (Tested on Python 3.14.7)
- **Terminal:** Any standard terminal emulator (macOS Terminal, iTerm2, Windows Terminal, PowerShell, or Linux bash/zsh)
- **Display Server:** An active graphical display environment (X11, Wayland, or macOS Quartz) to view Matplotlib chart windows

---

## 2. Installation & Setup

### Step 1: Clone the Repository
Clone the repository using Git:
```bash
git clone https://github.com/Kartik-idk/RetailPulse.git
cd RetailPulse
```

### Step 2: Create a Virtual Environment
Isolate project dependencies by setting up a Python virtual environment:
```bash
# On macOS and Linux:
python3 -m venv .venv
source .venv/bin/activate

# On Windows (Command Prompt):
python -m venv .venv
.venv\Scripts\activate.bat

# On Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
Install the required packages declared in `requirements.txt`:
```bash
pip install -r requirements.txt
```
*(RetailPulse requires only `matplotlib>=3.8.0`; all data processing uses Python's standard library).*

### Step 4: Verify Installation
Confirm that Python and Matplotlib are properly configured:
```bash
python3 -c "import matplotlib; print('Matplotlib version:', matplotlib.__version__)"
```

---

## 3. Running the Application

### Standard Execution
Launch the interactive terminal command center:
```bash
python main.py
```

### Execution with Custom Dataset Path
If your dataset is located in a different directory, supply the path as a command-line argument:
```bash
python main.py path/to/my_supermarket_sales.csv
```

### Display Help Information
To view usage flags and argument syntax:
```bash
python main.py --help
```

---

## 4. Navigating the Terminal Menu

When launched, RetailPulse loads the default dataset `dataset/supermarket_sales.csv`, prints an executive summary banner, and displays the main menu:

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

[+] Active Dataset : supermarket_sales.csv (/path/to/supermarket_sales.csv)
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
Enter your choice [1-10]: 
```

### Detailed Menu Walkthrough

#### Option 1: View Complete Visual Dashboard
- Prints the executive KPI summary table in the terminal.
- Opens the multi-chart Matplotlib master dashboard in a separate window.
- **Tip:** You can resize, maximize, or use Matplotlib's native pan/zoom and save tools.
- Closing the window automatically returns you to the terminal menu.

#### Option 2: Monthly Revenue Analysis
- Displays a chronological performance table with Monthly Revenue, % Share, Order Volume, and Units Sold.
- Launches the `Monthly Revenue Trend` line chart showing revenue progression over January, February, and March 2019.

#### Option 3: Product Category Analysis
- Displays category revenue rankings and gross profit contribution per line.
- Launches the horizontal bar chart showing category rankings from highest to lowest.

#### Option 4: Branch Performance
- Displays comparative operational statistics for Branch Alex (Yangon), Branch Cairo (Mandalay), and Branch Giza (Naypyitaw).
- Launches the comparative bar chart displaying revenue, transaction volume, and average satisfaction ratings.

#### Option 5: Payment Method Analysis
- Displays the volume and revenue breakdown across Ewallet, Cash, and Credit Card payments.
- Launches the modern donut chart illustrating customer payment preferences.

#### Option 6: Customer Type Analysis
- Compares loyalty program members (`Member`) against standard shoppers (`Normal`).
- Launches the donut chart illustrating shopper volume and revenue share.

#### Option 7: Gross Income Analysis
- Displays total gross profit generated per merchandise line.
- Launches the mint-green bar chart comparing gross profit by category.

#### Option 8: Customer Rating Analysis
- Displays category-level customer satisfaction scores and rating bounds.
- Launches the horizontal rating analysis chart with an overall benchmark line (`6.97 ★`).

#### Option 9: Reload Dataset
- Refreshes the CSV file from disk without restarting the program.
- Allows specifying a new CSV file or pressing `[Enter]` to reload the currently active file.
- Re-runs all schema validations and updates all in-memory calculations.

#### Option 10: Exit Application
- Displays a friendly closing banner and exits cleanly back to your terminal prompt.

---

## 5. Understanding the Visual Dashboard

The master visual dashboard incorporates modern design principles:
- **Theme Palette:** Built on a dark navy canvas (`#0B1120`) with contrasting panel cards (`#151F32`), subtle borders (`#2A374A`), and bright accents (Electric Blue, Purple, Mint, Amber).
- **KPI Cards:** Top banner displaying Total Revenue (\$322,966.75), Transactions (1,000), Units Sold (5,510), Average Order Value (\$322.97), and Average Customer Rating (6.97 ★).
- **Subplots:** 6 complementary charts arranged in a 2×3 grid providing a 360-degree executive view of operations.

---

## 6. Running the Automated Test Suite

To verify system integrity and execute all 52 automated tests:
```bash
python3 -m unittest discover -s tests -v
```

Expected output:
```text
Ran 52 tests in 0.193s

OK
```

---

## 7. Troubleshooting Common Issues

### Issue 1: `ModuleNotFoundError: No module named 'matplotlib'`
- **Cause:** Dependencies were not installed in the active Python environment.
- **Solution:** Activate your virtual environment and run:
  ```bash
  pip install -r requirements.txt
  ```

### Issue 2: `FileNotFoundError: Dataset file not found at: ...`
- **Cause:** The dataset file is missing from `dataset/supermarket_sales.csv`.
- **Solution:** Ensure `supermarket_sales.csv` is located in the `dataset/` directory, or provide the exact path when running `main.py`:
  ```bash
  python main.py /path/to/supermarket_sales.csv
  ```

### Issue 3: Matplotlib GUI Window Does Not Open on Linux/WSL
- **Cause:** Headless Linux environments or Windows Subsystem for Linux (WSL) without an active X-Server.
- **Solution:** On WSL, install an X-server like VcXsrv or WSLg. To verify non-interactive generation, use the automated test suite or export to image files.

### Issue 4: Garbled Characters in Terminal ASCII Banner
- **Cause:** Terminal emulator encoding is set to ASCII instead of UTF-8.
- **Solution:** Ensure your terminal encoding is set to UTF-8 (`export LANG=en_US.UTF-8`).
