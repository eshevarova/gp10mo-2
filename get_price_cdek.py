import requests
import json
import zipfile
import io
from get_round import get_round50
from hashlib import md5
from datetime import datetime
from cdek_parameters import *
from params import *


def json_request(ver, date_now, login, password, sender_id, receiver_id, tariff, mode, goods, services):
    url = "http://api.cdek.ru/calculator/calculate_price_by_json.php"
    json_obj = json.dumps({
        'version': ver,
        'dateExecute': date_now,
        'authLogin': login,
        'secure': password,
        'senderCityId': sender_id,
        'receiverCityId': receiver_id,
        'tariffList': tariff,
        'modeId': mode,
        'goods': goods,
        'services': services
        })
    
    answer = requests.post(url, data=json_obj)
    response = answer.json()
    return response

def get_price(city_id):
    date_now = datetime.now().strftime('%Y-%m-%d')
    SECURE = ('%s&%s') % (date_now, TEST_PASSWORD)
    SECURE = md5(SECURE.encode('utf-8')).hexdigest()
    response1 = json_request(VERSION, date_now, TEST_LOGIN, SECURE, SENDER_CITY_ID,
        city_id, TARIFFS1, MODE_ID, GOODS, SERVICES)
    response2 = json_request(VERSION, date_now, TEST_LOGIN, SECURE, SENDER_CITY_ID,
        city_id, TARIFFS2, MODE_ID, GOODS, SERVICES)

    gift_price = 200

    try:
        price_cdek1 = get_round50(response1['result']['price']) + gift_price
    except KeyError:
        price_cdek1 = 0

    try:
        price_cdek2 = get_round50(response2['result']['price']) + gift_price
    except KeyError:
        price_cdek2 = 0

    if price_cdek1 == 0 or price_cdek2 == 0:
        return max(price_cdek1, price_cdek2)
    else:
        return min(price_cdek1, price_cdek2)


if __name__ == '__main__':
    print(get_price('44'))
