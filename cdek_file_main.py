from get_cities_file import get_file
import time

url = 'https://www.cdek.ru/website/edostavka/upload/custom/files/CDEK_city.zip'
while True:
    get_file(url)
    time.sleep(604800)
