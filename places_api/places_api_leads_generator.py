from places_api.places_api_client import PlacesApiClient
import region.utils as region_utils

class PlacesApiLeadsGenerator:
    """Generates leads using a recursive grid search to bypass API limits."""

    def __init__(self, key, enterprise_plan, budget):
        self.client = PlacesApiClient(key=key, enterprise_plan=enterprise_plan)
        self.budget = budget
        self.request_count = 0

    def split_section(self, section):
        """Splits a rectangular region into 4 equal quadrants"""
        lat_diff, long_diff = region_utils.lat_long_difference(section)
        mid_lat = section['low']['latitude'] + (lat_diff / 2.0)
        mid_long = section['low']['longitude'] + (long_diff / 2.0)

        # Define the 4 new quadrants
        return [
            {'low': section['low'], 'high': {'latitude': mid_lat, 'longitude': mid_long}}, # SW
            {'low': {'latitude': mid_lat, 'longitude': section['low']['longitude']}, 
             'high': {'latitude': section['high']['latitude'], 'longitude': mid_long}},    # NW
            {'low': {'latitude': section['low']['latitude'], 'longitude': mid_long}, 
             'high': {'latitude': mid_lat, 'longitude': section['high']['longitude']}},    # SE
            {'low': {'latitude': mid_lat, 'longitude': mid_long}, 'high': section['high']} # NE
        ]

    def recursive_search(self, text_query, section):
        """Recursively searches an area. If 60 results are found, it splits the area"""
        self.request_count += 1
        if self.request_count > self.budget:
            print("Budget reached. Stopping.")
            return []

        print(f"Searching section... (Total requests: {self.request_count})")

        results = self.client.get_places(search=text_query, bounds=section)

        # Google returns max 60. If we hit ~60 there's likely more data hidden
        if len(results) >= 60:
            print("Area too dense, splitting into quadrants...")
            quadrants = self.split_section(section)
            combined_results = {}

            for quad in quadrants:
                sub_leads = self.recursive_search(text_query, quad)
                for lead in sub_leads:
                    combined_results[lead['id']] = lead

            return list(combined_results.values())

        return results
