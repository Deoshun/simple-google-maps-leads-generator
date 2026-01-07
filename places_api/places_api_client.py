import places_api.utils as utils
import time

class PlacesApiClient:
    def __init__(self, key, enterprise_plan):
        self.url = 'https://places.googleapis.com/v1/places:searchText'
        self.request_body_template = {
            'pageSize': 20,
            'textQuery': '',
            'locationRestriction': {
                'rectangle': {}
            }
        }
        self.request_headers = {
            'content-type': 'application/json',
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.primaryTypeDisplayName,places.primaryType,places.types,places.location,places.id,nextPageToken',
            'X-Goog-Api-Key': key
        }
        if (enterprise_plan == True):
            self.request_headers['X-Goog-FieldMask'] += ',places.nationalPhoneNumber,places.websiteUri,places.rating,places.internationalPhoneNumber,places.regularOpeningHours,places.priceLevel,places.priceRange,places.userRatingCount'
        

    def parse_place(self, place):
        return {
            'id': place['id'],
            'address': place['formattedAddress'],
            'longitude': place['location']['longitude'],
            'latitude': place['location']['latitude'],
            'name': place['displayName']['text'],
            'types': place.get('types'),
            'primary_type': place.get('primaryType'),
            'national_number': place.get('nationalPhoneNumber'),
            'website_uri': place.get('websiteUri'),
            'rating_count': place.get('userRatingCount'),
            'open_hours': place.get('regularOpeningHours'),
            'rating': place.get('rating'),
            'international_number': place.get('internationalPhoneNumber'),
            'price_level': place.get('priceLevel'),
            'price_range': place.get('priceRange')
        }

    def get_places(self, search, bounds):
        request_body = self.request_body_template.copy()
        request_body['textQuery'] = search
        request_body['locationRestriction']['rectangle'] = bounds

        places = []
        token = ''

        while (len(places) <= 60):
            api_response = utils.http_post(self.url, request_body, self.request_headers)
            
            if not api_response:
                break

            new_places = api_response.get('places', [])
            places.extend(map(self.parse_place, new_places))
            

            token = api_response.get('nextPageToken')
            if not token:
                break

            request_body['pageToken'] = token
            time.sleep(1.5)

        return places
