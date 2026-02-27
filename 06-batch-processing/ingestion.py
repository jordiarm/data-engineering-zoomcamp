
import os
from urllib.request import urlretrieve

# URL_PREFIX = "https://d37ci6vzurychx.cloudfront.net/trip-data/"

# TAXI_TYPE = input("Enter Taxi Type: ")

# YEAR = input("Enter Year: ")

# for MONTH in range(1, 13):
#     URL = f"{URL_PREFIX}{TAXI_TYPE}_tripdata_{YEAR}-{MONTH:02d}.parquet"

#     LOCAL_PREFIX = f"data/raw/{TAXI_TYPE}/{YEAR}/{MONTH:02d}"
#     LOCAL_FILE = f"{TAXI_TYPE}_tripdata_{YEAR}-{MONTH:02d}.parquet"
#     LOCAL_PATH = f"{LOCAL_PREFIX}/{LOCAL_FILE}"

#     os.makedirs(LOCAL_PREFIX, exist_ok=True)
#     print(f"Downloading {URL} -> {LOCAL_PATH}")
#     urlretrieve(URL, LOCAL_PATH)

URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

LOCAL_PREFIX = f"data/raw/zone_lookup"
LOCAL_FILE = "zoone_lookup.csv"
LOCAL_PATH = f"{LOCAL_PREFIX}/{LOCAL_FILE}"

os.makedirs(LOCAL_PREFIX, exist_ok=True)
print(f"Downloading {URL} -> {LOCAL_PATH}")
urlretrieve(URL, LOCAL_PATH)