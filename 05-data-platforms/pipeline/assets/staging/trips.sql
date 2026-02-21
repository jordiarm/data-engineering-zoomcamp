/* @bruin

name: staging.trips
type: bq.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: date

columns:
  - name: pickup_datetime
    type: timestamp
    description: Date and time when the meter was engaged
    primary_key: true
    nullable: false
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: Date and time when the meter was disengaged
  - name: passenger_count
    type: integer
    description: Number of passengers in the vehicle
    checks:
      - name: non_negative
  - name: trip_distance
    type: float
    description: Trip distance in miles
    checks:
      - name: non_negative
  - name: total_amount
    type: float
    description: Total amount charged to passenger
  - name: payment_type_name
    type: string
    description: Payment method name from lookup table

custom_checks:
  - name: row_count_positive
    description: Ensures the staging table is not empty after load
    query: SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM staging.trips
    value: 1
    operator: "="

@bruin */

WITH deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY
                tpep_pickup_datetime,
                tpep_dropoff_datetime,
                pu_location_id,
                do_location_id,
                fare_amount,
                taxi_type
            ORDER BY extracted_at DESC
        ) AS _row_num
    FROM ingestion.trips
    WHERE tpep_pickup_datetime >= '{{ start_datetime }}'
      AND tpep_pickup_datetime <  '{{ end_datetime }}'
)

SELECT
    d.tpep_pickup_datetime  AS pickup_datetime,
    d.tpep_dropoff_datetime AS dropoff_datetime,
    d.passenger_count,
    d.trip_distance,
    d.pu_location_id        AS pickup_location_id,
    d.do_location_id        AS dropoff_location_id,
    d.ratecode_id           AS rate_code_id,
    d.payment_type,
    p.payment_type_name,
    d.fare_amount,
    d.extra,
    d.mta_tax,
    d.tip_amount,
    d.tolls_amount,
    d.improvement_surcharge,
    d.congestion_surcharge,
    d.total_amount,
    d.taxi_type
FROM deduplicated d
LEFT JOIN ingestion.payment_lookup p
    ON d.payment_type = p.payment_type_id
WHERE d._row_num = 1
  AND d.tpep_pickup_datetime IS NOT NULL
  AND d.trip_distance >= 0
