from cdek_utils import load_file, get_id, get_price


def cdek_delivery(city):
    load_file()
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
