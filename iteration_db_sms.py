from db import Clients, session, Sent, Received
from cdek_main import cdek_delivery
from smsc_api import *
import time
import datetime

def add_to_db(phone, name):

    client = session.query(Clients).filter(Clients.phone == phone).first()

    if not client:
        sms_id = 'not_send'
        new_client = Clients(phone=phone, name=name)
        session.add(new_client)
        session.commit()

        new_sms_id = Sent(phone=new_client.phone, sms_id=sms_id)
        session.add(new_sms_id)
        session.commit()


def db_check_date(num):
    """
    If there is a repeated request through the form, the difference in dates is checked

    :param num:
    :return:
    """
    client = session.query(Clients).filter(Clients.phone == num).first()
    current_date = datetime.date.today()
    return current_date - client.date_added >= datetime.timedelta(1)


def first_sms(num):
    """
    Send the very first sms
    :param num:
    :return:
    """
    sms_id = 'not_send'
    new_id = 'new'
    sent = session.query(Sent).filter(Sent.phone == num and Sent.sms_id == sms_id).first()
    if sent or db_check_date(num):
        sms = SMSC()
        message = sms_message(sms_id)
        sms.send_sms(num, message, id=new_id, sender='sms')
        sent.sms_id = new_id
        sent.client.date_added = datetime.date.today()  # обновление даты в табл клиента
        session.commit()


def sms_message(key, mes=None):
    """
    Возаращает один из ответов в диалоге с клиентом
    :param key: str dict key
    :param mes: str
    :return: str dict value
    """
    messages = {
                'not_send': 'Здравствуйте! Для расчета стоимости доставки отправьте в ответном СМС цифру 1, для получения счет-договора - цифру 2.',

                'new': [
                        'Укажите Ваш город.',
                        'Для приобретения как частное лицо отправьте в ответном СМС цифру 1, на организацию - цифру 2.',
                         'К сожалению, запрос не распознан. Вы можете позвонить нам прямо сейчас по телефону +79778088970.'

                ],

                'city': [
                        'Доставка в пределах МКАД - 700 руб. Для оплаты наличными при получении отправьте в ответном СМС цифру 1, для оплаты по счету - цифру 2.',
                        'Доставка по Нижнему Новгороду - 500 руб. Для оплаты наличными при получении отправьте в ответном СМС цифру 1, для оплаты по счету - цифру 2.'

                ],

                'org': [
                        'Укажите в ответном СМС Вашу электронную почту.',
                        'Отправьте карточку фирмы (реквизиты) на электронную почту shev91@list.ru. В теме письма укажите "Заказ с сайта 15000, подарок".',
                        'К сожалению, запрос не распознан. Вы можете позвонить нам прямо сейчас по телефону +79778088970.'
                ],

                'msk': [
                        'Отправьте в ответном СМС адрес доставки.',
                        'Для выставления счет-договора отправьте в ответном СМС Вашу электронную почту.',
                        'К сожалению, запрос не распознан. Вы можете позвонить нам прямо сейчас по телефону +79778088970.'
                ],

                'nn': [
                        'Отправьте в ответном СМС адрес доставки.',
                        'Для выставления счет-договора отправьте в ответном СМС Вашу электронную почту.',
                        'К сожалению, запрос не распознан. Вы можете позвонить нам прямо сейчас по телефону +79778088970.'
                ],

                'cdek': [
                        ['Доставка -', 'руб. Для выставления счет-договора отправьте в ответном СМС Вашу электронную почту.'],
                        'К сожалению, не удалось рассчитать доставку автоматически. Для расчета доставки менеджером отправьте Ваши ФИО, \
                        номер телефона и город на электронную почту shev91@list.ru. В теме укажите "Заказ с сайта 15000, подарок".'
                ],

                'address': 'Благодарим за Ваши ответы! В ближайшее время с Вами свяжется наш специалист для уточнения даты и времени доставки.',

                'email': 'Укажите в ответном СМС Ваши ФИО.',

                'fio': 'Благодарим за запрос. В ближайшее время счет-договор придет на Вашу электронную почту.',

                #'error': 'К сожалению, запрос не распознан. Вы можете позвонить нам прямо сейчас по телефону +79778088970.'
    }

    if mes == '1':
        return messages.get(key)[0]
    elif mes == '2':
        return messages.get(key)[1]
    elif key in ['new', 'org', 'msk', 'nn'] and mes not in ['1', '2']:
        return messages.get(key)[2]
    elif key == 'city' and mes == 'error':
        return messages.get('cdek')[1]
    elif key == 'city' and type(mes) is int:
        return '%s %s %s' % (messages.get('cdek')[0][0], price, messages.get('cdek')[0][1])
    else:
        return messages.get(key)


def send_sms(num, old_sms_id, new_sms_id, mes=None):
    """

    :param num:
    :param sms_id:
    :param mes:
    :return:
    """
    sms = SMSC()
    message = sms_message(old_sms_id, mes)
    sms.send_sms(num, message, id=new_sms_id, sender='sms')
    time.sleep(5)
    # получение статуса доставки если надо
    status = sms.get_status(new_sms_id, num)


def get_answers(sms_id, phone, mes):
    """
    GOD FUNCTION!

    :param sms_id:
    :param phone:
    :param mes:
    :return:
    """
    answer = Received(sms_id=sms_id, phone=phone, mes=mes)  # полученный ответ записываем в базу
    client = session.query(Clients).filter(Clients.phone == phone).first()  # получаем клиента для обновления таблицы
    sent = session.query(Sent).filter(Sent.phone == phone and Sent.sms_id == sms_id).first()  # отправл смс
    new_id = ''

    if sms_id == 'new':

        if mes.strip() == '1':
            '''
            "Укажите Ваш город."
            '''
            new_id = 'city'
            sent.sms_id = new_id
        elif mes.strip() == '2':
            '''
            Если планируете приобретение как частное лицо, пришлите
            в ответном СМС цифру 1, если на организацию цифру 2
            '''
            new_id = 'org'
            sent.sms_id = new_id
        else:
            '''
            "В ближайшее время наш специалист свяжется с Вами и ответит на все
            интересующие Вас вопросы."
            '''
            new_id = 'error'
            sent.sms_id = new_id

    elif sms_id == 'city':

        if mes.strip().title() == 'Москва':
            """
            Доставка по Мск 700 р 1 или 2
            """
            sent.sms_id = 'msk'
        elif mes.strip().title() == 'Нижний Новгород':
            '''
            Доставка по НН 500р 1 или 2
            '''
            sent.sms_id = 'nn'
        else:
            town = mes.strip().title()

            price_cdek = cdek_delivery(city)

            if price_cdek in ('Empty', 'Overload', 'No delivery'):
                mes = 'error'
                new_id = 'zapros!!!'
                sent.sms_id = new_id
            else:
                mes = price_cdek
                new_id = 'email'
                sent.sms_id = new_id

        client.city = town

    elif sms_id == 'msk' or sms_id == 'nn':

        if mes.strip() == '1':
            print('Запрос адреса доставки')
            sent.sms_id = 'address'
        elif mes.strip() == '2':
            print('Запрос  почты для счета')
            sent.sms_id = 'email'
        else:
            pass

    elif sms_id == 'address':
        'Благодарность'
        client.full_address = mes

    elif sms_id == 'email':
        '''
        ФИО
        '''
        sent.sms_id = 'fio'
        client.email = mes

    elif sms_id == 'fio':
        'Благодарность договор на почту'
        client.full_name = mes



    # дописать остальные кейсы
    send_sms(phone, sms_id, new_id, mes)

    session.add(answer)
    session.commit()



