import requests

from django.conf import settings

API_KEY = settings.IPSTACK_API_KEY

def get_geolocation_data(ip_address:str="37.30.100.73"):
    url = f"http://api.ipstack.com/{ip_address}?access_key={API_KEY}"
    return requests.get(url).json()