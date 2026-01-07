from math import pi, cos, radians

EARTH_RADIUS_MILES = 3963
ONE_DEGREE_LATITUDE_IN_MILES = (pi / 180) * EARTH_RADIUS_MILES

def one_mile_in_degrees_latitude():
    return 1 / ONE_DEGREE_LATITUDE_IN_MILES

def one_mile_in_degrees_longitude(latitude):
    return 1 / (ONE_DEGREE_LATITUDE_IN_MILES * cos(radians(latitude)))

def lat_long_difference(coordinates):
    lat_diff = abs(coordinates['high']['latitude'] - coordinates['low']['latitude'])
    long_diff = abs(coordinates['high']['longitude'] - coordinates['low']['longitude'])
    return lat_diff, long_diff

def validate_coordinates(max_long_in_miles, max_lat_in_miles, coordinates):
    lat_diff, long_diff = lat_long_difference(coordinates)
    latitude_mid_point = coordinates['low']['latitude'] + lat_diff * 0.5

    region_lat_in_miles = lat_diff * ONE_DEGREE_LATITUDE_IN_MILES
    region_long_in_miles = long_diff * (ONE_DEGREE_LATITUDE_IN_MILES* cos(radians(latitude_mid_point)))

    if region_lat_in_miles > max_lat_in_miles:
        raise ValueError(f'Region latitude is {region_lat_in_miles:.2f} miles (max {max_lat_in_miles})')
    if region_long_in_miles > max_long_in_miles:
        raise ValueError(f'Region longitude is {region_long_in_miles:.2f} miles (max {max_long_in_miles})')
