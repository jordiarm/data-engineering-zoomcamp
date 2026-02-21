"""@bruin
name: ingestion.trips

type: python

image: python:3.11

connection: gcp-default

materialization:
  type: table
  strategy: append


@bruin"""

import os
import json
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


def materialize():
    start_date = datetime.strptime(os.environ["BRUIN_START_DATE"], "%Y-%m-%d")
    end_date = datetime.strptime(os.environ["BRUIN_END_DATE"], "%Y-%m-%d")

    bruin_vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = bruin_vars.get("taxi_types", ["yellow"])

    frames = []
    current = start_date.replace(day=1)

    while current < end_date:
        year_month = current.strftime("%Y-%m")

        for taxi_type in taxi_types:
            url = f"{BASE_URL}/{taxi_type}_tripdata_{year_month}.parquet"
            print(f"Fetching {url}")

            response = requests.get(url)
            response.raise_for_status()

            df = pd.read_parquet(BytesIO(response.content))
            df["taxi_type"] = taxi_type
            df["extracted_at"] = datetime.now(timezone.utc)
            frames.append(df)

        current += relativedelta(months=1)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)
