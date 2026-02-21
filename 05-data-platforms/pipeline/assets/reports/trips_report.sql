/* @bruin

name: reports.trips_report
type: bq.sql

depends:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_date
  time_granularity: date

columns:
  - name: pickup_date
    type: date
    description: Trip pickup date
    primary_key: true
  - name: taxi_type
    type: string
    description: Type of taxi (yellow, green, etc.)
    primary_key: true
  - name: payment_type_name
    type: string
    description: Payment method name
    primary_key: true
  - name: total_trips
    type: int64
    description: Total number of trips
    checks:
      - name: non_negative
  - name: total_passengers
    type: int64
    description: Total number of passengers
    checks:
      - name: non_negative
  - name: avg_trip_distance
    type: float
    description: Average trip distance in miles
  - name: avg_fare_amount
    type: float
    description: Average fare amount in USD
  - name: total_revenue
    type: float
    description: Total revenue (sum of total_amount)

@bruin */

SELECT
    CAST(pickup_datetime AS DATE)   AS pickup_date,
    taxi_type,
    COALESCE(payment_type_name, 'Unknown') AS payment_type_name,
    COUNT(*)                        AS total_trips,
    SUM(passenger_count)            AS total_passengers,
    ROUND(AVG(trip_distance), 2)    AS avg_trip_distance,
    ROUND(AVG(fare_amount), 2)      AS avg_fare_amount,
    ROUND(SUM(total_amount), 2)     AS total_revenue
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime <  '{{ end_datetime }}'
GROUP BY
    CAST(pickup_datetime AS DATE),
    taxi_type,
    COALESCE(payment_type_name, 'Unknown')
