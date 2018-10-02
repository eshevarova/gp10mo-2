from get_price_cdek import get_price
from get_city_id import get_id

city = 'Москва'

city_id = get_id(city)

if city_id == 'Empty':
    print('Нет города в реестре')
elif city_id == 'Overload':
    print('Городов с таким названием несколько')
else:
    price = get_price(city_id)
    if price == 0:
        print('Доставка невозможна')
    else:
        print('Доставка будет столько-то рублей')


"""
оформить этот файл как функцию
подправить параметры для посылки в функции гет_прайс_сдэк
"""