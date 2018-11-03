from cdek_utils import get_id, get_price


def cdek_delivery(city):
    city_id = get_id(city)
    if city_id in ('Empty', 'Overload'):
        return city_id

    price = get_price(city_id)
    if price != 0:
        return price
    else:
        return 'No delivery'



if __name__ == '__main__':
    print(cdek_delivery('Ростов-на-Дону'))
