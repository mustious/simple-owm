import simple_owm
import argparse
import json
import sys
import os


def save_credentials(arr):
    with open('credentials.json', '+w') as file:
        json.dump(arr, file)


parser = argparse.ArgumentParser(description=' parses argument from command line '
                                             'to help collect current weather readings')
parser.add_argument('-s', action='store_true', default=False,
                    dest='save_key',
                    help='save the the API key')
parser.add_argument('--key', '-k', action='store', dest='api_key',
                    help='API key to access openweathermap APIs')

# mutually exclusive arguments to find weather information based on only one of either
# city name, coordinates, zipcode or city ID

weather_group = parser.add_mutually_exclusive_group()
weather_group.add_argument('--by_city', action='store', dest='city_name',
                           help='name of city to access weather information')
weather_group.add_argument('--by_coord', action='store', dest='coordinates',
                           help='tuple of coordinates to access weather information')
weather_group.add_argument('--by_zipcode', action='store', dest='zipcode',
                           help='zipcode of place to access weather information', type=int)
weather_group.add_argument('--by_city_id', action='store', dest='city_id',
                           help='city ID of place to access weather information', type=int)

# specific weather information to access
parser.add_argument('--all', action='store_true', dest='get_all_info', default=False,
                    help='gets all the weather information')
parser.add_argument('--weather', action='store_true', dest='get_weather_desc', default=False,
                    help='gets the weather description of the city')
parser.add_argument('--coord', action='store_true', dest='get_coordinates', default=False,
                    help='gets the coordinates of the city in form of (lon,lat)')
parser.add_argument('--lon', action='store_true', dest='get_longitude', default=False,
                    help='gets the latitude of the city')
parser.add_argument('--lat', action='store_true', dest='get_latitude', default=False,
                    help='gets the longitude of the city')
parser.add_argument('--pressure', action='store_true', dest='get_pressure', default=False,
                    help='gets the pressure of the city in hPa')
parser.add_argument('--humidity', action='store_true', dest='get_humidity', default=False,
                    help='get the humidity percentage')
parser.add_argument('--wind', action='store_true', dest='get_wind_speed', default=False,
                    help='gets the wind speed of the city in meter/sec')

arguments = parser.parse_args()
print(parser.parse_args())

# saves the api key for future usage
if arguments.save_key:
    key_dict = {'api_key': arguments.api_key}
    save_credentials(key_dict)

if arguments.api_key:
    print("api key is given", arguments.api_key)

else:
    try:
        with open('credentials.json', '+r') as file:
            credential_json = json.load(file)
        saved_api_key = credential_json['api_key']

        if saved_api_key == False:
            print("No API key is saved... kindly provide an API key")
            sys.exit()

    except FileNotFoundError:
        print("No API key is saved... kindly provide an API key")
        sys.exit()

    print("api key not given, gotten from credential file", saved_api_key)
