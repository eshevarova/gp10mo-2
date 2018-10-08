from get_cities_file import get_file
from datetime import timedelta, datetime

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
    return
