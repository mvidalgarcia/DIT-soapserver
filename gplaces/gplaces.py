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


# Iterate through each category fetching one result and saving it
def collect_one_place_each_category():
    ''' [INFO]: 20 results maximum each page
        Established coordinates: San Francisco Park centre = 43.361490,-5.850613 | radius = 7000 = 7km '''
    for category_types in CATEGORIES_TYPES:
        response = urlopen(get_gplaces_api_link_nearby(43.361490, -5.850613, 7000, GPLACES_API_KEY, category_types[0], 'json'))
        treat_gplaces_response(response, category_types)


# Most of the logic
def treat_gplaces_response(response, category_types):
    str_response = response.read().decode('utf-8')
    json_response = json.loads(str_response)
    if json_response['status'] == 'OK':
        date_print('Query working OK ...')
        # New place object
        current_place = c.factory.create("Place")
        results_count = len(json_response['results'])
        element = 0
        already_saved = False
        while element < results_count and not already_saved:
            json_place = json_response['results'][element]
            # check if place already exists in DB
            if c.service.gplaces_id_exists_in_category(json_place['id'], category_types[1]):
                date_print('Place gplaces_id=%s, name=%s already exists in category_id=%s.'
                           % (json_place['id'], json_place['name'], category_types[1]))
                element += 1
            # if place id not exists, save new place
            else:
                if 'photos' in json_place:  # if the selected place has photo save it
                    save_place_image(current_place, json_place)
                # Fill Place fields and save it
                fill_place_fields(current_place, json_place, category_types)
                already_saved = True
        # if no place was saved ...
        if not already_saved:
            # 20 results per query maximum (Google Places API)
            if element == 20 and 'next_page_token' in json_response:
                # Query next page of results
                date_print("Going to next page of results ...")
                # TODO Recursive call
                response = urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?&pagetoken='+json_response['next_page_token'])
                treat_gplaces_response(response, category_types)
            else:
                date_print("No more results available ...")
    else:
        date_print("ERROR: Some problem has happened in the query ...")


# Return API places link which search places nearby
def get_gplaces_api_link_nearby(lat, lng, radius, api_key, types, output_format):
    output_format = output_format.lower()
    if output_format == 'json' or output_format == 'xml':
        return 'https://maps.googleapis.com/maps/api/place/nearbysearch/'+output_format+'?types='+types+'&' \
                'location='+str(lat)+','+str(lng)+'&radius='+str(radius)+'&sensor=false&rankby=prominence&key='+api_key


# Return API places link which search photos by reference
def get_gplaces_api_link_photo(photo_reference, api_key):
    return 'https://maps.googleapis.com/maps/api/place/photo' \
           '?photoreference='+photo_reference+'&maxwidth=1600&sensor=false&key='+api_key


def strip_accents(s):
    return ''.join(char for char in unicodedata.normalize('NFD', s) if unicodedata.category(char) != 'Mn')


# Save binary image in a server folder to serve it as a static file
def save_place_image(current_place, json_place):
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


# Fill place fields and store the object y the database
def fill_place_fields(current_place, json_place, category_types):
    # Fill Place fields
    current_place.gplaces_id = json_place['id']
    current_place.name = json_place['name']
    current_place.lat = json_place['geometry']['location']['lat']
    current_place.lng = json_place['geometry']['location']['lng']
    current_place.address = json_place['vicinity']
    current_place.category_id = category_types[1]
    # If there's no rating, 0.0 is assigned
    current_place.rating = json_place['rating'] if 'rating' in json_place else 0.0
    print('[%s] Saving place ...' % datetime.datetime.now().strftime("%d-%m-%y %H:%m"))
    print(current_place)
    returned_val = c.service.put_place(current_place)
    print('[%s] Place id=%s saved.' % (datetime.datetime.now().strftime("%d-%m-%y %H:%m"), returned_val))


def date_print(statement):
    print("[%s] %s" % (datetime.datetime.now().strftime("%d-%m-%y %H:%m"), statement))
