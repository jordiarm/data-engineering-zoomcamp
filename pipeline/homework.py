#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine

@click.command()
@click.option("--pg-user", default="root", help="PostgreSQL user")
@click.option("--pg-pass", default="root", help="PostgreSQL password")
@click.option("--pg-host", default="localhost", help="PostgreSQL host")
@click.option("--pg-port", default="5432", help="PostgreSQL port")
@click.option("--pg-db", default="ny_taxi", help="PostgreSQL database name")
@click.option("--target-table-taxi", default="green_taxi_data", help="Target table name")
@click.option("--target-table-zones", default="taxi_zone_lookup", help="Target table name")
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table_taxi, target_table_zones):

    url_green_taxi = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    url_zones = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

    df_green = pd.read_parquet(url_green_taxi)
    df_zones = pd.read_csv(url_zones)

    engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")

    df_green.head(0).to_sql(name=target_table_taxi, con=engine, if_exists="replace")
    df_green.to_sql(name=target_table_taxi, con=engine, if_exists="append")
    df_zones.head(0).to_sql(name=target_table_zones, con=engine, if_exists="replace")
    df_zones.to_sql(name=target_table_zones, con=engine, if_exists="append")





if __name__ == "__main__":
    main()

