with dim_zones_lookup as (
    select * from {{ref("taxi_zone_lookup")}}
),

renamed as (
    select
        cast(locationid as integer) as location_id,
        cast(borough as string) as borough,
        cast(zone as string) as zone,
        cast(service_zone as string) as service_zone
    from dim_zones_lookup
)

select * from renamed