
with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),

renamed as (
    select
        -- identifiers
        cast(dispatching_base_num as string) as dispatching_base_num,
        cast(pulocationid as integer) as pickup_location_id,
        cast(dolocationid as integer) as dropoff_location_id,

        -- timestamps
        cast(pickup_datetime as datetime) as pickup_datetime,
        cast(dropoff_datetime as datetime) as dropoff_datetime,

        -- trip info
        cast(SR_Flag as integer) as sr_flag,
        cast(Affiliated_base_number as string) as affiliated_base_number,
    from source
)

select
    *
from renamed
where date(pickup_datetime) >= '2019-01-01'
and date(pickup_datetime) < '2020-01-01'
and dispatching_base_num is not null