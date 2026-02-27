from pyspark.sql import SparkSession, DataFrame

from pyspark.sql import functions as F


def create_trips_df(spark:SparkSession) -> DataFrame:

    df_yellow = (
        spark.read.parquet("/Users/jordiarmentia/data-engineering-zoomcamp/06-batch-processing/data/raw/yellow/*/*")
        .withColumnsRenamed(
            {
                "lpep_pickup_datetime" : "pickup_datetime",
                "lpep_dropoff_datetime" : "dropoff_datetime",
            }
        )
    )

    df_green = (
        spark.read.parquet("/Users/jordiarmentia/data-engineering-zoomcamp/06-batch-processing/data/raw/green/*/*")
        .withColumnsRenamed(
            {
                "lpep_pickup_datetime" : "pickup_datetime",
                "lpep_dropoff_datetime" : "dropoff_datetime",
            }
        )
    )

    common_cols = []
    yellow_cols = set(df_yellow.columns)

    for col in df_green.columns:
        if col in yellow_cols:
            common_cols.append(col)

    df_green_select = (
        df_green
        .select(*common_cols)
        .withColumn("service_type", F.lit("green"))
    )

    df_yellow_select = (
        df_yellow
        .select(*common_cols)
        .withColumn("service_type", F.lit("yellow"))
    )

    return (
        df_green_select
        .unionAll(df_yellow_select)
    )

