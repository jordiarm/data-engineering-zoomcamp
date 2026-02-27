from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from .daily_report_transforms import (
    get_date_columns,
    add_payment_types,
    add_vendor_id
)
from .daily_report_config import BaseConfig, YellowDailyReportConfig, GreenDailyReportConfig


def create_yellow_daily_report(df: DataFrame, start_date: str, end_date: str) -> DataFrame:

    """Creates the daily NY Yellow Taxi Report for given dates"""

    return (
        df
        .transform(get_date_columns, YellowDailyReportConfig.DATE_COLS)
        .where(F.col("tpep_pickup_date").between(start_date, end_date))
        .withColumnsRenamed(
            {
                "tpep_pickup_datetime" : "pickup_datetime",
                "tpep_dropoff_datetime" : "dropoff_datetime",
                "tpep_pickup_date" : "pickup_date",
                "tpep_dropoff_date" : "dropoff_date",
            }
        )
        .withColum("taxi_type", F.lit("yellow"))
        .transform(add_payment_types, BaseConfig.PAYMENT_TYPE)
        .transform(add_vendor_id, BaseConfig.VENDOR_ID)
        .groupBy(BaseConfig.GROUPBY_COLS)
        .agg(
            F.count("*").alias("trip_count"),
            *[F.round(F.sum(col), 2).alias(f"total_{col}") for col in BaseConfig.AGG_COLS],
            *[F.max(col).alias(f"max_{col}") for col in BaseConfig.AGG_COLS]
        )
    )


def create_green_daily_report(df:DataFrame, start_date: str, end_date: str) -> DataFrame:
    """Creates the daily NY Green Taxi Report for given dates"""

    return (
        df
        .transform(get_date_columns, GreenDailyReportConfig.DATE_COLS)
        .where(F.col("lpep_pickup_date").between(start_date, end_date))
        .withColumnsRenamed(
            {
                "lpep_pickup_datetime" : "pickup_datetime",
                "lpep_dropoff_datetime" : "dropoff_datetime",
                "lpep_pickup_date" : "pickup_date",
                "lpep_dropoff_date" : "dropoff_date",
            }
        )
        .withColum("taxi_type", F.lit("green"))
        .transform(add_payment_types, BaseConfig.PAYMENT_TYPE)
        .groupBy(BaseConfig.GROUPBY_COLS)
        .agg(
            F.count("*").alias("trip_count"),
            *[F.round(F.sum(col), 2).alias(f"total_{col}") for col in BaseConfig.AGG_COLS],
            *[F.max(col).alias(f"max_{col}") for col in BaseConfig.AGG_COLS]
        )
    )

