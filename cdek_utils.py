import requests
import json
import zipfile
import io
import xlwt
import os
import shutil
from hashlib import md5
from xlrd import open_workbook
from datetime import datetime, timedelta
from xlutils.copy import copy
from project_files.cdek_parameters import *


def get_file(url):
    result = requests.get(url)
    file_zip = zipfile.ZipFile(io.BytesIO(result.content))
    folder = zipfile.ZipFile.namelist(file_zip)[0]

    new_path = os.getcwd()

    if os.path.exists(folder):
        shutil.rmtree(folder)

    if os.path.exists('CDEK_city.xls'):
        os.unlink('CDEK_city.xls')

    file_zip.extractall()

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if 'RUS' not in file_path:
            os.unlink(file_path)
        else:
            shutil.move(file_path, os.path.join(new_path, the_file))
            os.rename(os.path.join(new_path, the_file), os.path.join(new_path, 'CDEK_city.xls'))
    os.rmdir(folder)


def load_file():
    url = 'https://www.cdek.ru/website/edostavka/upload/custom/files/CDEK_city.zip'
    with open('date.txt', 'r', encoding='utf-8') as f:
        date_start = f.read()
    date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
    date_now = datetime.today().date()
    delta = date_now - date_start
    week = timedelta(days=7)
    if delta > week:
        get_file(url)
        with open('date.txt', 'w', encoding='utf-8') as f:
            f.write(date_now.strftime('%Y-%m-%d'))


def get_id(city):
    filename = 'CDEK_city.xls'
    file_path = os.path.join(os.getcwd(), filename)

    work_book = open_workbook(file_path)
    work_sheet = work_book.sheet_by_index(0)

    names_num = 0
    for row in range(1, work_sheet.nrows):
        if isinstance(work_sheet.cell_value(row, 2), str):
            if city == work_sheet.cell_value(row, 2).split(', ')[0]:
                names_num += 1
                city_id = work_sheet.cell_value(row, 0)
            else:
                continue
    if names_num == 0:
        return 'Empty'
    elif names_num == 1:
        return str(int(city_id))
    elif names_num > 1:
        return 'Overload'


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


def get_round50(str_num):
    try:
        num = int(str_num)
    except ValueError:
        num = int(float(str_num))
    round_to_ceil = 50
    div, mod = divmod(num, round_to_ceil)
    if mod == 0:
        return num
    else:
        return (div + 1) * round_to_ceil


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
