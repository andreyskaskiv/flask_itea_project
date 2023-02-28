import requests


def get_ip():
    url = 'https://api.ipify.org/?format=json'
    response = requests.get(url)
    return response.json()['ip']


def get_geo_data(ip: str):
    url = f'https://ipapi.co/{ip}/json/'
    response = requests.get(url)
    return response.json()


def main():
    ip = get_ip()
    geo_data = get_geo_data(ip)
    return geo_data['city']


#
# ip = get_ip()
# print(ip)
# print(get_geo_data(ip))
