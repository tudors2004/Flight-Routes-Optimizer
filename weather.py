import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://dir.aviapages.com/api/metars/'
headers = {
    'Authorization': f'Token {API_KEY}'
}

def get_weather(icao_codes):
    if not icao_codes:
        return {}
    icao_str = ",".join(icao_codes)
    params = {
        'icao': icao_str,
        'decode': 'true'
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    try:
        json_data = response.json()
        return json_data
    except requests.exceptions.JSONDecodeError:
        return {}