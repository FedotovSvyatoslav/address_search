import requests
from io import BytesIO
from PIL import Image
import sys


def get_object_scale(lower_corner, upper_corner):
    leftdown_angle = tuple(map(float, lower_corner.split()))
    rightup_angle = tuple(map(float, upper_corner.split()))
    width_degrees = abs(rightup_angle[0] - leftdown_angle[0])
    height_degrees = abs(rightup_angle[1] - leftdown_angle[1])
    return f"{width_degrees},{height_degrees}"


toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if response:
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    area = toponym["boundedBy"]["Envelope"]

    scale = get_object_scale(area["lowerCorner"], area["upperCorner"])

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": scale,
        "l": "map",
        "pt": "{0},{1},pm2dgl".format(toponym_longitude, toponym_lattitude)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(response.content)).show()
