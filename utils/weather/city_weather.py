import requests


def get_weather(city: str, app_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={app_key}&units=metric'
    response = requests.get(url)
    return response.json()


def get_weather_icon_url(icon_name: str):
    icon_url = f'http://openweathermap.org/img/wn/{icon_name}@2x.png'
    return icon_url


def parse_weather_data(city_weather: dict):
    icon_name = city_weather['weather'][0]['icon']
    country_code = city_weather['sys']['country']

    icon_url = get_weather_icon_url(icon_name)
    latitude = city_weather['coord']['lat']
    longitude = city_weather['coord']['lon']
    sky = city_weather['weather'][0]['description']
    temperature = city_weather['main']['temp']
    wind_speed = city_weather['wind']['speed']

    weather_data = {
        'icon_url': icon_url,
        'latitude': latitude,
        'longitude': longitude,
        'sky': sky,
        'temperature': temperature,
        'wind_speed': wind_speed,
        'country': country_code}
    return weather_data


def main(city: str, app_key):
    city_weather = get_weather(city, app_key)
    if 'message' not in city_weather:
        return parse_weather_data(city_weather)
    return city_weather



