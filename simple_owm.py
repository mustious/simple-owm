import requests


class CurrentWeather:
    """
    a simple python to help consume current weather information api from https://openweathermap.org
    """

    def __init__(self, api_key: str):
        """
        :param api_key: API key provided by openweathermap
        :ivar self.api_key: API key
        :ivar self.weather_json: json from the api call
        :ivar self.own_url: openweathermap url generated based on call type e.g loacation, coordinate, zip codes
        """

        self.api_key = api_key  # api key from openweathermap
        self.weather_json = None
        self.owm_url = None

    def by_city(self, city: str):
        """
        check weather info by city name

        :param city: name of the city to check weather info
        :return:
        """
        url_template_city = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        self.owm_url = url_template_city.format(city_name=city, api_key=self.api_key)
        self.__get_json(self.owm_url)

    def by_coord(self, coord: tuple):
        """
        checks current weather info by coordinates
        :param coord: coordinate of a particular city
        :return:
        """
        url_template_coord = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        self.owm_url = url_template_coord.format(lat=coord[0], lon=coord[1], api_key=self.api_key)
        self.__get_json(self.owm_url)

    def by_zipcode(self, zip_code: int, country_code: str = 'US'):
        """
        checks current weather information by zip codes together with country code

        :param zip_code: zip code of the desired location
        :param country_code: country code, defaults to USA when not specified
        :return:
        """
        url_template_zip = "https://api.openweathermap.org/data/2.5/weather?" \
                           "zip={zip_code},{country_code}&appid={api_key}"
        self.owm_url = url_template_zip.format(zip_code=zip_code, country_code=country_code, api_key=self.api_key)
        self.__get_json(self.owm_url)

    def by_city_ID(self, city_ID: int):
        """
        unambiguous weather infomation by using city ID

        :param city_id: unique ID of city
        :return:
        """
        url_template_cityID = "https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}"
        self.owm_url = url_template_cityID.format(city_id=city_ID, api_key=self.api_key)
        self.__get_json(self.owm_url)

    def __get_json(self, owm_url: str):
        """

        :param own_url:
        :return: json of the api call
        """
        try:
            owm_request = requests.get(owm_url)

            # checks weather a request is 'OK' else raises an error
            if owm_request.status_code == 200:
                print(owm_request.status_code)
                owm_json = owm_request.json()
                self.weather_json = owm_request.json()
                print(owm_json)
                return owm_json

            else:
                error_json = owm_request.json()
                error_code = error_json['cod']
                error_message = error_json['message']
                error_full = "{} error - {}".format(error_code, error_message)
                raise NameError(error_full)

        except:
            raise

    def url(self):
        """
        obtains the openweathermap url used for api call based on selected parameters

        :return: openweathermap url
        :rtype: str
        """
        return self.owm_url

    def temp(self, kind: str='temp'):
        """
        returns the average temperature, when 'kind=temp_max' returns the maximum temperature
        when 'kind=temp_min' returns the minimum temperature

        :param kind: type of temperature
        :return:
        :rtype: float
        """

        if kind == 'temp':
            temp = self.weather_json['main']['temp']
            return temp
        elif kind == 'temp_max':
            temp_max = self.weather_json['main']['temp_max']
            return temp_max
        else:
            temp_min = self.weather_json['main']['temp_min']
            return temp_min

    def weather(self):
        """
        returns a group of weather parameter and a description of the weather condition
        :return:
        """
        weather = self.weather_json['weather'][0]
        main = weather['main']
        description = weather['description']
        return main, description

    def coord(self):
        """
        obtains the coordinate of the used location
        :return: coordinates of the location
        :rtype: tuple
        """
        coord_dict = self.weather_json['coord']  # dictionary containing values of longitude and latitude
        coord_ = tuple(coord_dict.values())
        return coord_

    def longitude(self):
        """
        returns the longitude value of the selected location
        :return: longitude
        :rtype: float
        """
        longitude = self.get_coord()[0]
        return longitude

    def latitude(self):
        """
        returns the latitude value of the selected location
        :return: latitude
        :rtype: float
        """
        latitude = self.get_coord()[1]
        return latitude

    def pressure(self):
        """
        Atmospheric temperature measured in hPa (hectopascals)
        :return: pressure
        :rtype: float
        """
        pressure = self.weather_json['main']['pressure']
        return pressure

    def humidity(self):
        """
        Humidity of the current location in
        :return: Humidity
        :rtype: float
        """
        humidity = self.weather_json['main']['humidity']
        return humidity

    def wind(self):
        """
        obtains the wind speed (default: meter/sec) and the wind direction in degrees
        :return: speed, degree
        :rtype: float, int
    """
        speed = self.weather_json['wind']['speed']
        degree = self.weather_json['wind']['deg']
        return speed, degree

current = CurrentWeather(api_key='sgreg34rgf3t').by_city('kogi')
print(current.wind())