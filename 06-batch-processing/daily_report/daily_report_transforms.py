from typing import List
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

# def format_license_num (df: DataFrame)-> DataFrame:

#     num = F.regexp_extract(F.col("hvfhs_license_num"), r"(\d+)", 1)

#     return (
#         df
#         .withColumn(
#             "formated_lic_num",
#             F.when(
#                 num.cast("int") % 2 == 0,
#                 F.concat(F.lit("s/"), num)
#             )
#             .otherwise(
#                 F.concat(F.lit("e/"), num)
#             )
#         )

#     )

def get_date_columns(df: DataFrame, cols:List[str]) -> DataFrame:

    for col in cols:
        date_col = col.replace("_datetime", "_date")
        df = df.withColumn(date_col, F.to_date(col))

    return df

def add_payment_types(df: DataFrame, payment_type_map: dict) -> DataFrame:

    mapping_expr = F.create_map(
        *[item for k, v in payment_type_map.items() for item in (F.lit(k), F.lit(v))]
    )

    return df.withColumn("payment_type_description", mapping_expr[F.col("payment_type")])

def add_vendor_id(df: DataFrame, vendor_id_map: dict) -> DataFrame:
    mapping_expr = F.create_map(
        *[item for k, v in vendor_id_map.items() for item in (F.lit(k), F.lit(v))]
    )

    return df.withColumn("vendor_name", mapping_expr[F.col("VendorID")])


