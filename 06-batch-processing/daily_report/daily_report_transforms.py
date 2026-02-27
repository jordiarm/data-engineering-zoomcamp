from typing import List
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def format_license_num (df: DataFrame)-> DataFrame:

    num = F.regexp_extract(F.col("hvfhs_license_num"), r"(\d+)", 1)

    return (
        df
        .withColumn(
            "formated_lic_num",
            F.when(
                num.cast("int") % 2 == 0,
                F.concat(F.lit("s/"), num)
            )
            .otherwise(
                F.concat(F.lit("e/"), num)
            )
        )

    )

def get_date_columns(df: DataFrame, cols:List[str]) -> DataFrame:

    for col in cols:
        date_col = col.replace("_datetime", "_date")
        df = df.withColumn(date_col, F.to_date(col))

    return df