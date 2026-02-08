-- Creating external table referring to gcs path

CREATE OR REPLACE EXTERNAL TABLE `meta-imagery-484316-j9.zoomcamp.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://module_03_zoomcamp/yellow_tripdata_2024-*.parquet']
);

-- Creating regular non-partitioned table in BQ using the yellow taxi trip records

CREATE OR REPLACE TABLE `meta-imagery-484316-j9.zoomcamp.yellow_tripdata_non_partitioned` AS
select * from meta-imagery-484316-j9.zoomcamp.external_yellow_tripdata;

select count(distinct PULocationID)
from meta-imagery-484316-j9.zoomcamp.external_yellow_tripdata;

select count(distinct PULocationID)
from meta-imagery-484316-j9.zoomcamp.yellow_tripdata_non_partitioned;

select count(PULocationID) from meta-imagery-484316-j9.zoomcamp.yellow_tripdata_non_partitioned where fare_amount = 0;

--creating partitioned and clustered table
CREATE OR REPLACE TABLE `meta-imagery-484316-j9.zoomcamp.yellow_tripdata_part_clust`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
select * from meta-imagery-484316-j9.zoomcamp.external_yellow_tripdata;


select distinct VendorID
from meta-imagery-484316-j9.zoomcamp.yellow_tripdata_non_partitioned
where DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

select distinct VendorID
from meta-imagery-484316-j9.zoomcamp.yellow_tripdata_part_clust
where DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';


select count(*) from meta-imagery-484316-j9.zoomcamp.yellow_tripdata_non_partitioned;

