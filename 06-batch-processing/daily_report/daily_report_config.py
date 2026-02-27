from pyspark.sql import types


class BaseConfig:

    VENDOR_ID = {
        1 : "Creative Mobile Technologies, LLC",
        2 : "Curb Mobility, LLC",
        6 : "Myle Technologies Inc",
        7 : "Helix",
    }

    PAYMENT_TYPE = {
        0 : "Flex Fare trip",
        1 : "Credit card",
        2 : "Cash",
        3 : "No charge",
        4 : "Dispute",
        5 : "Unknown",
        6 : "Voided trip",
    }

    RATE_CODE_ID = {
        1 : "Standard rate",
        2 : "JFK",
        3 : "Newark",
        4 : "Nassau or Westchester",
        5 : "Negotiated fare",
        6 : "Group ride",
        99 : "Null/unknown",
    }


class YellowDailyReportConfig:

    DATE_COLS = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]

    GROUPBY_COLS = [
        "tpep_pickup_date",
        "tpep_dropoff_date",
        # "VendorID",
        "vendor_name",
        "PULocationID",
        "DOLocationID",
        # "payment_type",
        "payment_type_description",
        "store_and_fwd_flag",
    ]

    AGG_COLS = [
        "trip_distance",
        "fare_amount",
        "tip_amount",
        # "trip_time",
        # "sales_tax",
        # "congestion_surcharge",
        # "base_passenger_fare",
    ]

class GreenDailyReportConfig:

    DATE_COLS = [
        "lpep_pickup_datetime",
        "lpep_dropoff_datetime",
    ]

    GROUPBY_COLS = [

    ]

    AGG_COLS = [

    ]

