from pyspark.sql import types


class BaseConfig:

    VENDOR_ID: dict = {
        1 : "Creative Mobile Technologies, LLC",
        2 : "Curb Mobility, LLC",
        6 : "Myle Technologies Inc",
        7 : "Helix",
    }

    PAYMENT_TYPE: dict = {
        0 : "Flex Fare trip",
        1 : "Credit card",
        2 : "Cash",
        3 : "No charge",
        4 : "Dispute",
        5 : "Unknown",
        6 : "Voided trip",
    }

    RATE_CODE_ID: dict = {
        1 : "Standard rate",
        2 : "JFK",
        3 : "Newark",
        4 : "Nassau or Westchester",
        5 : "Negotiated fare",
        6 : "Group ride",
        99 : "Null/unknown",
    }

    GROUPBY_COLS: list[str] = [
        "tpep_pickup_date",
        "tpep_dropoff_date",
        "VendorID",
        "vendor_name",
        "PULocationID",
        "DOLocationID",
        "payment_type",
        "payment_type_description",
        "store_and_fwd_flag",
    ]

    AGG_COLS: list[str] = [
        "trip_distance",
        "fare_amount",
        "tip_amount",
    ]


class YellowDailyReportConfig:

    DATE_COLS: list[str] = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]

class GreenDailyReportConfig:

    DATE_COLS: list[str] = [
        "lpep_pickup_datetime",
        "lpep_dropoff_datetime",
    ]
    