from urllib.request import urlopen
import json
#import requests

gplaces_api_key = 'AIzaSyAdZKWV1F9NBWVSk7YbCyf-7_NuM7jmFf8';

response = urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?types=grocery_or_supermarket|store&location=43.363965,-5.852354&radius=7000&sensor=false&key='+gplaces_api_key)
#response = requests.get('https://maps.googleapis.com/maps/api/place/photo?photoreference=CnRnAAAABpkwwZCp-qL2et8-j2p1I8R7FbAM_Q9YY_F4t8-VDWRCGncE66rNSOVF2u9XvDMQIJDNI-pFMOp6nLKYjOZdV4yHGDHedQBilWPmycNB8OQUzOr4yhwK2lazxsh2dzstYHnHxP7q-7hzJZPok85dGBIQhKARrqiqqYw77AxA2utvqxoUj77ajoCp3NdgDtUN9ERIbhSPCYY&maxwidth=1600&sensor=false&key='+gplaces_api_key)
print(response.read().decode('utf-8'))
#obj = json.loads(response.decode('utf-8'))
#data = response.read()

#fp = open('image.png', 'wb')
#fp.write(response.content)
#fp.close
#print(obj)
