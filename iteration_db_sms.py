from db import Clients, session, Sent, Received
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
                        'В ближайшее время наш специалист свяжется с Вами.'
                ],

                'city': [
                        'Доставка в пределах МКАД - 700 руб. Для оплаты наличными при получении отправьте в ответном СМС цифру 1, для оплаты по счету - цифру 2.',
                        'Доставка по Нижнему Новгороду - 500 руб. Для оплаты наличными при получении отправьте в ответном СМС цифру 1, для оплаты по счету - цифру 2.',
                ],

                'org': [
                        'Укажите в ответном СМС Вашу электронную почту.',
                        'Отправьте карточку фирмы (реквизиты) на электронную почту shev91@list.ru. В теме письма укажите "Заказ с сайта 15000, подарок".',
                        'К сожалению, запрос не распознан. Вы можете позвонить нам прямо сейчас по телефону +79778088970.'
                ],

                'msk': [
                        'Отправьте в ответном СМС адрес доставки.',
                        'Для выставления счет-договора отправьте в ответном СМС Вашу электронную почту.'
                ],

                'nn': [
                        'Отправьте в ответном СМС адрес доставки.',
                        'Для выставления счет-договора отправьте в ответном СМС Вашу электронную почту.'
                ],

                'cdek': [
                        'Доставка до города N - *** руб. Для выставления счет-договора отправьте в ответном СМС Вашу электронную почту.',
                        'К сожалению, в указанном Вами городе отсутствуют филиалы СДЭК. тут дописать'
                ],

                'address': 'Благодарим за Ваши ответы! В ближайшее время с Вами свяжется наш специалист для уточнения даты и времени доставки.',

                'email': 'Укажите в ответном СМС Ваши ФИО.',

                'fio': 'Благодарим за запрос. В ближайшее время счет-договор придет на Вашу электронную почту.',
    }
    if mes == '1':
        return messages.get(key)[0]
    elif mes == '2':
        return messages.get(key)[1]
    elif mes == 'Erunda': # для непонятной хрени если надо или убрать
        return messages.get(key)[2]
    else:
        return messages.get(key)


def send_sms(num, sms_id, mes=None):
    """

    :param num:
    :param sms_id:
    :param mes:
    :return:
    """
    sms = SMSC()
    message = sms_message(sms_id, mes)
    sms.send_sms(num, message, id=sms_id, sender='sms')
    time.sleep(5)
    # получение статуса доставки если надо
    status = sms.get_status(sms_id, num)


def get_answers(sms_id, phone, mes):
    """
    GOD FUNCTION!

    :param sms_id:
    :param phone:
    :param mes:
    :return:
    """
    answer = Received(sms_id=sms_id, phone=phone, mes=mes)  # полученный ответ записываем в базу
    client = session.query(Clients).filter(Clients.phone == phone).first() # получаем клиента для обновления таблицы
    sent = session.query(Sent).filter(Sent.phone == phone and Sent.sms_id == sms_id).first() # отправл смс

    if sms_id == 'new':

        if mes.strip() == '1':
            '''
            "Укажите Ваш город."
            '''
            sent.sms_id = 'city'
        elif mes.strip() == '2':
            '''
            Если планируете приобретение как частное лицо, пришлите
            в ответном СМС цифру 1, если на организацию цифру 2
            '''
            print('Запрос формы организации %s' % phone)
            sent.sms_id = 'org'
        else:
            '''
            "В ближайшее время наш специалист свяжется с Вами и ответит на все
            интересующие Вас вопросы."
            '''

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
            # проверка на сдэк
            pass
        client.city = mes.strip().title()

    elif sms_id == 'msk' or sms_id == 'nn':

        if mes.strip() == '1':
            print('Запрос адреса доставки')
            sent.sms_id = 'address'
        elif mes.strip() == '2':
            print('Запрос  почты для счета')
            sent.sms_id = 'email'

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

    session.add(answer)
    session.commit()



