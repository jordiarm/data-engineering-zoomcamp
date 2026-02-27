from pyspark.sql import types


class DailyReportConfig():

    PATH = "/Users/jordiarmentia/data-engineering-zoomcamp/06-batch-processing/fhvhv/2021/01/"

    SCHEMA = types.StructType([
        types.StructField('dispatching_base_num', types.StringType(), True),
        types.StructField('originating_base_num', types.StringType(), True),
        types.StructField('request_datetime', types.TimestampType(), True),
        types.StructField('on_scene_datetime', types.TimestampType(), True),
        types.StructField('pickup_datetime', types.TimestampType(), True),
        types.StructField('dropoff_datetime', types.TimestampType(), True),
        types.StructField('PULocationID', types.LongType(), True),
        types.StructField('DOLocationID', types.LongType(), True),
        types.StructField('trip_miles', types.DoubleType(), True),
        types.StructField('trip_time', types.LongType(), True),
        types.StructField('base_passenger_fare', types.DoubleType(), True),
        types.StructField('tolls', types.DoubleType(), True),
        types.StructField('bcf', types.DoubleType(), True),
        types.StructField('sales_tax', types.DoubleType(), True),
        types.StructField('congestion_surcharge', types.DoubleType(), True),
        types.StructField('airport_fee', types.DoubleType(), True),
        types.StructField('tips', types.DoubleType(), True),
        types.StructField('driver_pay', types.DoubleType(), True),
        types.StructField('shared_request_flag', types.StringType(), True),
        types.StructField('shared_match_flag', types.StringType(), True),
        types.StructField('access_a_ride_flag', types.StringType(), True),
        types.StructField('wav_request_flag', types.StringType(), True),
        types.StructField('wav_match_flag', types.StringType(), True),
        types.StructField('hvfhs_license_num', types.StringType(), True),
    ])

    DATE_COLS = [
        "pickup_datetime",
        "dropoff_datetime",
        "request_datetime",
        "on_scene_datetime",
    ]

    GROUPBY_COLS = [
        "pickup_date",
        "PULocationID",
        "hvfhs_license_num"

    ]

    AGG_COLS = [
        "trip_miles",
        "trip_time",
        "sales_tax",
        "congestion_surcharge",
        "base_passenger_fare",
    ]

