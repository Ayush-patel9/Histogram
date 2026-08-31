# DBMS Assignment 1 - Histogram
The github link for this project is -> https://github.com/Ayush-patel9/Histogram.git
This repository contains the code and generated figures for **Assignment 1: Histogram** on the Join Order Benchmark (JOB) database.

## Prerequisites

- **PostgreSQL Engine**: Version 16 or above is recommended.
- **Python**: Version 3.x.
- **Database**: The JOB database must be loaded in PostgreSQL with the database name `job`.
- **Database User**: By default, the Python scripts connect using the user `ayushpatel`. If your local PostgreSQL setup uses a different username, please edit the `DB_USER` variable at the top of `code/histogram.py` and `code/selectivity.py`.

## System Setup (Python & pip)

If your system does not already have Python and `pip` installed, follow the OS-specific instructions below to install them. Otherwise, you can skip to **Environment Setup**.

### Windows
1. Download the latest Python installer from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer. **CRITICAL:** Make sure to check the box that says **"Add Python to PATH"** at the bottom of the installer window before clicking "Install Now".
3. Open a new Command Prompt or PowerShell and verify installation by running: `python --version` and `pip --version`.

### macOS
1. Open the Terminal.
2. The easiest way to install Python is via [Homebrew](https://brew.sh/). If you don't have Homebrew, install it first:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python
   ```
4. Verify installation by running: `python3 --version` and `pip3 --version`.

### Linux (Ubuntu/Debian)
1. Open the Terminal.
2. Update your package list and install Python and pip:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```
3. Verify installation by running: `python3 --version` and `pip3 --version`.

## Environment Setup

To run the Python scripts, it is highly recommended to use a virtual environment. Follow the steps below to set up your environment and install the necessary requirements.

**Note about libraries:** The `requirements.txt` file intentionally only includes third-party packages (`psycopg2-binary` and `matplotlib`). Libraries like `time` and `collections` are part of the **Python Standard Library** and are already built into Python by default, so they do not need to be installed via `pip`. Furthermore, `scipy` is explicitly **not** used in this codebase; the code implements a custom pure-Python linear regression function specifically to minimize heavy external dependencies.

1. Open your terminal.
2. Navigate to the root directory of this project:
   ```bash
   do pwd to find the directory and do cd /path/to/your/directory
   ```
3. Create a Python virtual environment named `venv`:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
5. Install the required dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Execution Instructions

To run all scripts automatically and generate all plots at once, use the `main.py` script provided in the root directory:

```bash
python main.py
```

Alternatively, you can run each script individually. All scripts are stored in the `code/` directory and are designed to run in a single command, automatically generating the required plots and printing results to the console. Make sure your virtual environment is activated and you are in the `code/` directory before running them.

```bash
cd code/
```

- **Run plot1.py**: 
  ```bash
  python plot1.py
  ```
- **Run plot2.py**: 
  ```bash
  python plot2.py
  ```
- **Run histogram.py**: 
  ```bash
  python histogram.py
  ```
- **Run selectivity.py**: 
  ```bash
  python selectivity.py
  ```

## Code Descriptions & Assignment Mapping

Below is a detailed breakdown of what each script does, which part of the assignment it solves, and the outputs it generates.

### `plot1.py`
- **Purpose**: Plots an equi-depth histogram for the `id` column of the `title` table using boundaries predefined from PostgreSQL `pg_stats`.
- **Assignment Mapping**: Answers **Q1 (Part 6)** by displaying the histogram as a bar-plot with value-boundaries on the X-axis and frequency on the Y-axis.
- **Figures Generated**: Displays a matplotlib figure window titled **"Equi-Depth Histogram for title.id"**.

### `plot2.py`
- **Purpose**: Plots an equi-depth histogram for the textual `title` column of the `title` table using text boundaries from PostgreSQL `pg_stats`.
- **Assignment Mapping**: Answers **Q1 (Part 6)** by showing the textual attribute histogram as a bar-plot with lexicographically ordered value-boundaries on the X-axis and frequency on the Y-axis.
- **Figures Generated**: Displays a matplotlib figure window titled **"Equi-Depth Histogram for title.title"**.

### `histogram.py`
Change the DB_USER and bucket_size and no of sample in the top .
- **Purpose**: Fetches 3000 random samples from the `title` table (using `TABLESAMPLE BERNOULLI`) for both the `id` and `title` columns. It then calculates an optimal serial histogram of 19 buckets using dynamic programming to minimize Sum of Squared Errors (SSE). It also extrapolates the time required to build the histogram on the full table using linear regression on pre-recorded build times for 1000, 3000, and 5000 samples.
- **Assignment Mapping**:
  - **Q2 (Part 1)**: Visualizes the optimal serial histograms as a bar-plot.
  - **Q2 (Part 2 & 3)**: Calculates and prints the exact time taken to build the histograms and lists the frequency bucket boundaries in the console.
  - **Q2 (Part 5 & 6)**: Contains data points for sample size vs. time and calculates linear regression to extrapolate the time for the full table (`2,528,312` rows), outputting the extrapolated times.
  - **Q2 (Part 7)**: Generates plots showing the relationship between sample size and histogram build time, including extrapolated full table time.
- **Figures Generated**: 
  1. A side-by-side bar plot window showing the **"Optimal Serial Histogram for id"** and **"Optimal Serial Histogram for title"**.
  2. A plot showing **"Sample Size vs Histogram Build Time"** for 1000, 3000, and 5000 samples.
  3. A log-scaled plot showing **"Extrapolated Sample Size vs Histogram Build Time"** predicting the time for the entire dataset.

### `selectivity.py`
- **Purpose**: Computes the maximum selectivity error for both `id` and `title` columns over varying sample sizes (1000, 3000, and 5000) using dynamic programming.
- **Assignment Mapping**: Answers **Q2 (Part 4 & 8)** by printing out the maximum selectivity error to the console for each sample size and generating a line plot depicting the relationship between sample size and max selectivity error.
- **Figures Generated**: Displays a matplotlib figure window titled **"Sample Size vs Maximum Selectivity Error"**.

---
*Note: Any figures saved during the execution or from previous runs are stored in the `figures/` directory.*

