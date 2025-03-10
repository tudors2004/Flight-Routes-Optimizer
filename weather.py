import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://aviapages.com/api/weather/metar/'

headers = {
    'Authorization': f'Token {API_KEY}'
}







def get_weather(iata_codes, iata_to_icao_mapping):
    icao_codes = []
    for iata_code in iata_codes:
        icao_code = iata_to_icao_mapping.get(iata_code.upper())
        if icao_code:
            icao_codes.append(icao_code)
        else:
            return {'raw_metar': f"No ICAO mapping found for {iata_code}"}

    params = {
        'icao': ','.join(icao_codes),
        'decode': 'true'
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        weather_data = {}
        for icao_code in icao_codes:
            if icao_code in data and data[icao_code]:
                weather_data[icao_code] = data[icao_code][0]
            else:
                weather_data[icao_code] = f"No METAR data available for {icao_code}"

        return weather_data
    except requests.exceptions.HTTPError as err:
        return {'raw_metar': f"Error {response.status_code}: {err}"}
    except Exception as err:
        return {'raw_metar': f"Unexpected error: {err}"}