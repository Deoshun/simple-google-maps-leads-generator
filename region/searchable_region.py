from region import utils
from math import ceil

class SearchableRegion:
    def __init__(self, coordinates):
        utils.validate_coordinates(25, 25, coordinates)
        self.sections = self._generate_sections(coordinates)

    def _generate_sections(self, coordinates):
        latitude_difference, longitude_difference = utils.lat_long_difference(coordinates)
        latitude_mid_point = min(coordinates['low']['latitude'], coordinates['high']['latitude']) + latitude_difference * 0.5

        vertical_points_count = ceil(latitude_difference / utils.one_mile_in_degrees_latitude())
        horizontal_points_count = ceil(longitude_difference / utils.one_mile_in_degrees_longitude(latitude_mid_point))

        lat_step = latitude_difference / vertical_points_count
        long_step = longitude_difference / horizontal_points_count

        start_long = min(coordinates['low']['longitude'], coordinates['high']['longitude'])
        start_lat = min(coordinates['low']['latitude'], coordinates['high']['latitude'])
        
        long_points = [round(start_long + long_step * i, 6) for i in range(horizontal_points_count + 1)]
        lat_points = [round(start_lat + lat_step * i, 6) for i in range(vertical_points_count + 1)]

        index = 0
        sections = []
        for i in range(len(long_points) - 1):
            for j in range(len(lat_points) - 1):
                sections.append({
                    'id': index, 
                    'coordinates': {
                        'low': {
                            'longitude': long_points[i],
                            'latitude': lat_points[j]
                        },
                        'high': {
                            'longitude': long_points[i + 1],
                            'latitude': lat_points[j + 1]
                        }
                    }
                })
                index += 1
        return sections
