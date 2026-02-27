# Module 6 – Batch Processing

## Overview

This module covers batch data processing using **Apache Spark (PySpark)**. The main application is a daily report pipeline that reads FHVHV (For-Hire Vehicle) parquet data, applies transformations, and aggregates trip metrics by date, pickup location, and license number.

## Tech Stack

- **Python 3.11**
- **PySpark 4.1.1+** – distributed batch processing
- **pandas 3.0.1+** – auxiliary data manipulation
- **PyArrow 23.0.1+** – efficient parquet I/O
- **Jupyter** – interactive notebooks
- **uv** – package manager

## Directory Structure

```
06-batch-processing/
├── CLAUDE.md
├── pyproject.toml              # Project dependencies (managed with uv)
├── uv.lock
├── .python-version             # Python 3.11
├── main.py                     # Root placeholder entry point
├── test_spark.py               # Manual Spark smoke test
├── 04_pyspark.ipynb            # PySpark learning notebook
├── daily_report/
│   ├── main.py                 # Pipeline entry point
│   ├── daily_report.py         # Core pipeline logic
│   ├── daily_report_config.py  # Schema, paths, and column config
│   ├── daily_report_transforms.py  # Pure transformation functions
│   └── batch_processing_tests_plan.md  # Testing strategy
└── reports/                    # Output directory (empty)
```

## Setup

```bash
cd 06-batch-processing
uv sync
```

Requires **Java** to be available for Spark. The pipeline sets `JAVA_HOME` automatically at runtime.

## Running the Pipeline

```bash
# Run the daily report pipeline
cd 06-batch-processing
uv run python daily_report/main.py

# Basic Spark smoke test
uv run python test_spark.py

# Open the learning notebook
uv run jupyter notebook 04_pyspark.ipynb
```

## Pipeline Logic (`daily_report/`)

### Entry point: `daily_report/main.py`
- Creates a `SparkSession` (local mode)
- Calls `create_daily_report(spark)` and displays the result

### Core pipeline: `daily_report/daily_report.py`
`create_daily_report(spark)` does the following:
1. Reads parquet files from `DailyReportConfig.PATH` using the defined schema
2. Applies `format_license_num` – reformats `hvfhs_license_num` (e.g. `HV0002` → `s/2`, `HV0003` → `e/3`)
3. Applies `get_date_columns` – converts timestamp columns to date columns
4. Groups by `pickup_date`, `PULocationID`, `hvfhs_license_num`
5. Aggregates `trip_miles`, `trip_time`, `sales_tax`, `congestion_surcharge`, `base_passenger_fare`

### Transforms: `daily_report/daily_report_transforms.py`

| Function | Description |
|---|---|
| `format_license_num(df)` | Extracts number from license string; prefixes `s/` (even) or `e/` (odd) |
| `get_date_columns(df, cols)` | Converts `*_datetime` columns to `*_date` date columns |

### Config: `daily_report/daily_report_config.py`
- `PATH` – path to parquet input data (update this for your environment)
- `SCHEMA` – 24-field `StructType` for FHVHV data
- `DATE_COLS` – timestamp columns to convert to dates
- `GROUPBY_COLS` – aggregation dimensions
- `AGG_COLS` – columns to sum/max

## Testing

No automated tests exist yet. A detailed plan is in `daily_report/batch_processing_tests_plan.md`.

The plan proposes:
- `pytest` with a **session-scoped `SparkSession` fixture** to avoid JVM overhead
- Unit tests for each transform in `tests/test_transforms.py`
- Integration test for the full pipeline in `tests/test_daily_report.py`
- Monkeypatching `DailyReportConfig.PATH` with a temporary directory for integration tests

To run tests once implemented:
```bash
uv run pytest tests/ -v
```

## Data

The pipeline expects **FHVHV parquet files** partitioned by year/month. Update `DailyReportConfig.PATH` to point to your local data:

```
fhvhv/
└── 2021/
    └── 01/
        └── *.parquet
```

Sample data can be downloaded from the [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) page.
