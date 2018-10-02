import requests
import json
import zipfile
import io
from get_round import get_round50

def get_price(city_id):
    url = "http://api.cdek.ru/calculator/calculate_price_by_json.php"
    json_obj = json.dumps({'version': '1.0', 'senderCityId': '414', 'receiverCityId': city_id,
                            'tariffId': '62', 'modeId': '4', 'goods': [{'weight': '18',
                            'length': '50', 'width': '50', 'height': '50'}], 'services':
                            [{'id': '2', 'param': '15000'}]})
    answer = requests.post(url, data=json_obj)
    response = answer.json()
    gift_price = 200
    try:
        price_cdek = get_round50(response['result']['price']) + gift_price
        return price_cdek
    except KeyError:
        return 0
