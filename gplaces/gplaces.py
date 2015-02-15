__author__ = 'Marco Vidal Garcia'

from urllib.request import urlopen
import json
import requests
import shutil
import socket  # to get my own ip
import datetime  # to get timestamp
import unicodedata


from suds.client import Client

has_permissions = True
c = Client('http://localhost:8888/?wsdl')


GPLACES_API_KEY = 'AIzaSyAdZKWV1F9NBWVSk7YbCyf-7_NuM7jmFf8'

# Categories -> Google Places types
EATING_TYPES = 'food|restaurant|meal_takeaway'
HANGOUTS_TYPES = 'night_club|bar|cafe'
LEISURE_TYPES = 'casino|library|movie_theater|museum|zoo|amusement_park|stadium'
PERSONAL_CARE_TYPES = 'spa|gym|hair_care|beauty_salon'
RELIGION_TYPES = 'church|cemetery|hindu_temple|funeral_home|synagogue|mosque'
SHOPPING_TYPES = 'shopping_mall|store|establishment|grocery_or_supermarket|book_store|' \
                 'clothing_store|convenience_store|convenience_store|electronics_store|' \
                 'bicycle_store|furniture_store|hardware_store|home_goods_store|jewelry_store|' \
                 'liquor_store|pet_store|shoe_store'
# (type, category_id)
CATEGORIES_TYPES = [(EATING_TYPES, 1), (HANGOUTS_TYPES, 2), (LEISURE_TYPES, 3),
                    (PERSONAL_CARE_TYPES, 4), (RELIGION_TYPES, 5), (SHOPPING_TYPES, 6)]


def get_gplaces_api_link_nearby(lat, lng, radius, api_key, types, output_format):
    output_format = output_format.lower()
    if output_format == 'json' or output_format == 'xml':
        return 'https://maps.googleapis.com/maps/api/place/nearbysearch/'+output_format+'?types='+types+'&' \
                'location='+str(lat)+','+str(lng)+'&radius='+str(radius)+'&sensor=false&rankby=prominence&key='+api_key


def get_gplaces_api_link_photo(photo_reference, api_key):
    return 'https://maps.googleapis.com/maps/api/place/photo' \
           '?photoreference='+photo_reference+'&maxwidth=1600&sensor=false&key='+api_key


def strip_accents(s):
    return ''.join(char for char in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


# Save one place of each category in the database
def save_places():
    # 20 results maximum
    # San Francisco Park centre coordinate = 43.361490,-5.850613 | radius = 7000 = 7km
    # Iterate through each category fetching one result and saving it
    for category_types in CATEGORIES_TYPES:
        response = urlopen(get_gplaces_api_link_nearby(43.361490, -5.850613, 7000, GPLACES_API_KEY, category_types[0], 'json'))

        str_response = response.read().decode('utf-8')
        #print(str_response)
        json_response = json.loads(str_response)

        if json_response['status'] == 'OK':
            print('[%s] Query working OK ...' % datetime.datetime.now().strftime("%d-%m-%y %H:%m"))
            # New place object
            current_place = c.factory.create("Place")
            results_count = len(json_response['results'])
            element = 0
            already_saved = False
            while element < results_count and not already_saved:
                json_place = json_response['results'][element]
                if c.service.gplaces_id_exists(json_place['id']):  # check if place already exist in DB
                    print('[%s] Place gplaces_id=%s, name=%s already exists.' % (datetime.datetime.now().strftime("%d-%m-%y %H:%m"), json_place['id'], json_place['name']))
                    element += 1
                else:  # if place id not exists, save new place
                    if 'photos' in json_place:  # if the selected place has photo save it
                        photo_reference = json_place['photos'][0]['photo_reference']
                        # Photo query
                        photo_response = requests.get(get_gplaces_api_link_photo(photo_reference, GPLACES_API_KEY), stream=True)
                        if photo_response.status_code == 200:  # if response 200 OK
                            photo_name = strip_accents(json_place['name'])
                            photo_name = photo_name.replace(' ', '_')+'_'+datetime.datetime.now().strftime("%d-%m-%y_%H.%m")+'.jpg'
                            with open('/srv/images/'+photo_name, 'wb') as f:
                                shutil.copyfileobj(photo_response.raw, f)

                            # Watch out the port!
                            current_place.image = 'http://'+socket.gethostbyname(socket.gethostname())+':8080/images/'+photo_name

                    # Fill Place fields
                    current_place.gplaces_id = json_place['id']
                    current_place.name = json_place['name']
                    current_place.lat = json_place['geometry']['location']['lat']
                    current_place.lng = json_place['geometry']['location']['lng']
                    current_place.address = json_place['vicinity']
                    current_place.category_id = category_types[1]
                    print('[%s] Saving place ...' % datetime.datetime.now().strftime("%d-%m-%y %H:%m"))
                    print(current_place)
                    retval = c.service.put_place(current_place)
                    print('[%s] Place id=%s saved.' % (datetime.datetime.now().strftime("%d-%m-%y %H:%m"), retval))
                    already_saved = True

            # if no place was saved ...
            if not already_saved:
                # 20 results per query maximum (Google Places API)
                if element == 20:
                    # Query next page of results
                    # TODO
                    print("[%s] Going to next page of results ..." % datetime.datetime.now().strftime("%d-%m-%y %H:%m"))
                else:
                    print("[%s] No more results available ..." % datetime.datetime.now().strftime("%d-%m-%y %H:%m"))

        else:
            print("[%s] ERROR: Some problem has happened in the query ..." % datetime.datetime.now().strftime("%d-%m-%y %H:%m"))
