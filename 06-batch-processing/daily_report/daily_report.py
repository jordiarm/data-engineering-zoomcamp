from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from daily_report_transforms import (
    format_license_num,
    get_date_columns
)
from daily_report_config import DailyReportConfig


# TODO: Add date filter parameter (start_date, end_date) to scope the report
# to a specific date range. Filter should be applied on `pickup_date` before
# the groupBy aggregation for efficiency.
def create_daily_report(spark: SparkSession) -> DataFrame:

    df = spark.read.schema(DailyReportConfig.SCHEMA).parquet(DailyReportConfig.PATH)

    return (
        df
        .transform(format_license_num)
        .transform(get_date_columns, DailyReportConfig.DATE_COLS)
        .withColumn("pickup_date", F.to_date("pickup_datetime"))
        .groupBy(DailyReportConfig.GROUPBY_COLS)
        .agg(
            *[F.sum(col).alias(f"total_{col}") for col in DailyReportConfig.AGG_COLS],
            *[F.max(col).alias(f"max_{col}") for col in DailyReportConfig.AGG_COLS]
        )
    )



