from pyspark.sql import SparkSession, DataFrame

from daily_report_transforms import format_license_num
from daily_report_config import DailyReportConfig


def create_daily_report(spark: SparkSession) -> DataFrame:

    df = spark.read.schema(DailyReportConfig.SCHEMA).parquet(DailyReportConfig.PATH)

    return (
        df
        .transform(format_license_num)
    )



