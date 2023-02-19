import requests

WEATHER_API_KEY = 'd9fd45b2d7ea8f80d8ab154815efdf41'
OPENWEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appId}&units=metric'


def get_weather(weather_url: str, api_key: str, city: str):
    """
    @param str weather_url: Parametrized openweather url
    @param api_key: Api key
    @param city: City name
    @return str: Weather condition

    Reference: https://openweathermap.org/current
    """
    weather_condition = ''
    url = weather_url.format(
        city=city,
        appId=api_key
    )

    response = requests.get(url)
    if response.status_code != 200:
        message = 'openweathermap.org returned non-200 code. Actual code is {code}, message is: {message}'.format(
            code=str(response.status_code),
            message=response.json()['message']
        )
        raise RuntimeError(message)

    return response.json()


if __name__ == '__main__':
    # print(get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona'))
    print('-' * 50)
    print(f"Temperature = {get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona')['main']['temp']} Celsius\n"
          f"Temperature feels like = {get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona')['main']['feels_like']} Celsius\n"
          f"Atmospheric pressure = {get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona')['main']['pressure']}  hPa\n"
          f"Humidity = {get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona')['main']['humidity']} % \n"
          f"Visibility = {get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona')['visibility']} meter \n"
          f"Wind speed = {get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona')['wind']['speed']} meter/sec \n"
          f"Country code = {get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona')['sys']['country']} \n"
          )

"""
Temperature = 16.89 Celsius
Temperature feels like = 15.94 Celsius
Atmospheric pressure = 1028  hPa
Humidity = 50 % 
Visibility = 10000 meter 
Wind speed = 1.54 meter/sec 
Country code = ES 
"""
