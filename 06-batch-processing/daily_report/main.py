import os
from pyspark.sql import SparkSession
from daily_report import create_daily_report

os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17"

spark = (
    SparkSession
    .builder
    .master("local[*]")
    .appName("daily_report")
    .getOrCreate()
)

df = create_daily_report(spark)
df.show()
