from server.models import db
from sqlalchemy.sql import text
from datetime import timedelta, datetime, date
from typing import Dict

Dates: dict = {
    "week": 7,
    "month": 30,
    "3 month": 90,
    "6 month": 180,
    "9 month": 270,
    "year": 365
}

def five_closest_stations(latitude: float, longitude: float) -> list:
    query = text(
        '''
        select t1.id, t1.name, t1.line, t1.latitude, t1.longitude from (
            select id, name, line, latitude, longitude, acos( sin( radians(:lat) ) * sin( radians(latitude) ) + cos( radians(:lat) ) * cos( radians(latitude) ) * cos( radians(:lon - longitude) ) ) * 3958.756 as distance from stations order by distance limit 5
        ) as t1
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, lat=latitude, lon=longitude).fetchall()

    return results

def stations_within_half_mile(latitude: float, longitude: float) -> list:
    query = text(
        '''
        select t1.id, t1.name, t1.line, t1.latitude, t1.longitude from (
            select id, name, line, latitude, longitude, acos( sin( radians(:lat) ) * sin( radians(latitude) ) + cos( radians(:lat) ) * cos( radians(latitude) ) * cos( radians(:lon - longitude) ) ) * 3958.756 as distance from stations
        ) as t1 where distance < 0.5
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, lat=latitude, lon=longitude).fetchall()

    return results

def crimes_near_station(station_id: int, range: int) -> list:
    query = text(
        '''
        select t3.crime_date, t3.pd_desc, t3.ofns_desc, t3.latitude, t3.longitude, t4.category from (
           select t2.* from crimes_by_station as t1 join crime_info as t2 on t1.crime_id = t2.id where t1.station_id = 1 and t2.crime_date > current_date - 365
        ) as t3 join crime_categories as t4 on t3.category_id = t4.id
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, id=station_id, range=range)

    return results
    

def crimes_near_point(latitude: float, longitude: float, categories: tuple, range: int) -> list:

    query = text(
        '''
        select t1.crime_date, t2.category, t1.ofns_desc, t1.pd_desc, t1.latitude, t1.longitude from crime_info as t1 join crime_categories as t2 on t1.category_id = t2.id where acos( sin( radians(:lat) ) * sin( radians(latitude) ) + cos( radians(:lat) ) * cos( radians(latitude) ) * cos( radians( :lon - longitude) ) ) * 6371 < 0.1524 and t1.category_id = any(:cat) and t1.crime_date > current_date - :range
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, lat=latitude, lon=longitude, cat=categories, range=range).fetchall()

    return results

def station_percentile_rank(station_ids: tuple, categories: tuple, range: int) -> list:
    query = text(
        '''
         with subquery as (
            select t7.id, t7.name, t7.line, coalesce(t7.sum, 0) as sum, t7.count from (
                select t5.id, t5.name, t5.line, sum(t6.risk_points), count(t6.category) from stations as t5 left join (
                    select * from crimes_by_station as t3 join (
                        select t1.category, t1.risk_points, t2.id from crime_categories as t1 join crime_info as t2 on t1.id = t2.category_id where t1.id = any(:cat) and t2.crime_date > current_date - :range
                    ) as t4 on t3.crime_id = t4.id
                ) as t6 on t5.id = t6.station_id group by t5.id
            ) as t7
        )
        select t1.id, t1.name, t1.line, t1.sum / cast(t2.max as float) * 100 as percentile from subquery as t1 join (select max(coalesce(subquery.sum, 0)) from subquery) as t2 on true where t1.id = any(:cat) order by percentile
        '''
    ) if len(station_ids) > 0 else text(
        '''
        with subquery as (
            select t7.id, t7.name, t7.line, coalesce(t7.sum, 0) as sum, t7.count from (
                select t5.id, t5.name, t5.line, sum(t6.risk_points), count(t6.category) from stations as t5 left join (
                    select * from crimes_by_station as t3 join (
                        select t1.category, t1.risk_points, t2.id from crime_categories as t1 join crime_info as t2 on t1.id = t2.category_id where t1.id = any(:cat) and t2.crime_date > current_date - :range
                    ) as t4 on t3.crime_id = t4.id
                ) as t6 on t5.id = t6.station_id group by t5.id
            ) as t7
        )
        select t1.id, t1.name, t1.line, t1.sum / cast(t2.max as float) * 100 as percentile from subquery as t1 join (select max(coalesce(subquery.sum, 0)) from subquery) as t2 on true order by percentile
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, cat=categories, range=range, s_id=station_ids) if len(station_ids) > 0 else conn.execute(query, cat=categories, range=range).fetchall()

    return results

# Give Crime Category IDs
# For each station display occurences for given ids

def crime_category_occurrence_all_stations(categories: tuple, range: int) -> list:
    query = text(
        '''
        select t7.id, t7.name, t7.line, t7.count from (
            select t5.id, t5.name, t5.line, sum(t6.risk_points), count(t6.category) from stations as t5 left join (
                select * from crimes_by_station as t3 join (
                    select t1.category, t1.risk_points, t2.id from crime_categories as t1 join crime_info as t2 on t1.id = t2.category_id where t1.id = any(:cat) and t2.crime_date > current_date - :range
                ) as t4 on t3.crime_id = t4.id
            ) as t6 on t5.id = t6.station_id group by t5.id
        ) as t7;
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, cat=categories, range=range).fetchall()

    return results

# Give Station ID 
# Gives occurrences for each crime category
# Ex:
# For ID = 1
# Category    Occurrences
# Burglary         1
# .....

def crime_categories_occurrences_per_station(station_id: int, range: int) -> list:
    query = text(
        '''
        select t3.category, coalesce(sum(t4.category_id) / t4.category_id, 0) as occurrences from crime_categories as t3 left join (
            select t1.station_id, t2.category_id from crimes_by_station as t1 join crime_info as t2 on t1.crime_id = t2.id where t1.station_id = :s_id and t2.crime_date > current_date - :range
        ) as t4 on t3.id = t4.category_id group by t3.category, t4.category_id;
        '''
    )

    with db.connect() as conn:
        results = conn.execute(query, s_id=station_id, range=range)

    return results