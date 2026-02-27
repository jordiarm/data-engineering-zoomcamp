from pyspark.sql import SparkSession, DataFrame
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