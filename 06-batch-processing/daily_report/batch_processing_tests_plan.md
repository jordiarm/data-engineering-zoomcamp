# Plan: Add Batch Processing Tests for Module 6

## Context

The `06-batch-processing` module contains a PySpark daily-report pipeline that processes FHVHV (For-Hire Vehicle) trip data. There are currently no tests. We need to add unit tests for the two transform functions and an integration test for the full pipeline, so the code can be verified without depending on real data files.

---

## Files to Create / Modify

| Action | File |
|--------|------|
| Create | `06-batch-processing/tests/__init__.py` |
| Create | `06-batch-processing/tests/conftest.py` |
| Create | `06-batch-processing/tests/test_transforms.py` |
| Create | `06-batch-processing/tests/test_daily_report.py` |
| Modify | `06-batch-processing/pyproject.toml` (add `pytest` dev dependency) |

---

## Implementation Plan

### 1. `pyproject.toml` — add pytest

Add an `[dependency-groups]` section (uv convention) so `pytest` is available as a dev dependency:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
]
```

---

### 2. `tests/conftest.py` — shared SparkSession fixture

Create a session-scoped `spark` pytest fixture to avoid spinning up a new JVM for every test:

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder
        .master("local[1]")
        .appName("tests")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()
```

---

### 3. `tests/test_transforms.py` — unit tests for transform functions

**Imports:** `format_license_num`, `get_date_columns` from `daily_report.daily_report_transforms`.

#### `format_license_num` tests

| Test | Input `hvfhs_license_num` | Expected `formated_lic_num` |
|------|--------------------------|------------------------------|
| even number → `s/` prefix | `"HV0002"` | `"s/2"` |
| odd number  → `e/` prefix | `"HV0003"` | `"e/3"` |
| larger even | `"HV0100"` | `"s/100"` |
| null stays null | `None` | `None` |

Each test builds a small in-memory DataFrame, calls `format_license_num`, and asserts on the collected rows.

#### `get_date_columns` tests

| Test | Description |
|------|-------------|
| single column conversion | `pickup_datetime` (timestamp) → `pickup_date` (date) |
| correct date value | The date matches the timestamp's date part |
| original timestamp preserved | Source column still exists after transform |
| multiple columns | Both `pickup_datetime` and `dropoff_datetime` converted in one call |

---

### 4. `tests/test_daily_report.py` — integration test for `create_daily_report`

Since `create_daily_report` reads from a hardcoded path in `DailyReportConfig.PATH`, we:
1. Write a small synthetic DataFrame to a **temporary directory** as parquet (using a `tmp_path` pytest fixture).
2. Monkeypatch `DailyReportConfig.PATH` to that temp directory.
3. Call `create_daily_report(spark)` and assert on the result.

**Synthetic data rows (2 days × 2 groups → 3 unique aggregated rows):**

| pickup_datetime | PULocationID | hvfhs_license_num | trip_miles | trip_time | … |
|---|---|---|---|---|---|
| 2021-01-01 08:00 | 100 | HV0002 | 5.0 | 600 | … |
| 2021-01-01 10:00 | 100 | HV0002 | 3.0 | 400 | … |
| 2021-01-01 08:00 | 200 | HV0003 | 7.0 | 900 | … |
| 2021-01-02 09:00 | 100 | HV0002 | 4.0 | 500 | … |

**Assertions:**

| Test | What it checks |
|------|----------------|
| `test_output_columns_exist` | All expected columns present: `pickup_date`, `PULocationID`, `hvfhs_license_num`, `total_trip_miles`, `max_trip_miles`, etc. |
| `test_groupby_aggregation_sums` | For (2021-01-01, 100, HV0002): `total_trip_miles` == 8.0, `total_trip_time` == 1000 |
| `test_groupby_aggregation_max` | Same group: `max_trip_miles` == 5.0, `max_trip_time` == 600 |
| `test_row_count` | 3 output rows (3 unique date/location/license combos) |
| `test_license_format_applied` | `formated_lic_num` column exists and values follow `s/` / `e/` pattern |

---

## Running the Tests

```bash
cd 06-batch-processing
uv run pytest tests/ -v
```

---

## Key Design Decisions

- **No external test libraries** (e.g., chispa) — plain pytest + PySpark to keep deps minimal.
- **Session-scoped SparkSession** — avoids JVM startup overhead per test.
- **Monkeypatch PATH** — lets us integration-test `create_daily_report` without real data files or modifying production code.
- **Small synthetic data** — deterministic, easy to reason about expected values.
