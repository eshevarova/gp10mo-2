from db import Clients, session, Sent, Received, Bills
from cdek_main import cdek_delivery
from bill_excel import get_bill
from email_file import send_attachment
from project_files.bill_parameters import FIRST_NUMBER
from project_files.mail_parameters import TO_WHOM_EMAIL
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

                'error': 'К сожалению, запрос не распознан. Вы можете позвонить нам прямо сейчас по телефону +79778088970.'
    }

    if mes == '1':
        return messages.get(key)[0]
    elif mes == '2':
        return messages.get(key)[1]
    elif key in ['new', 'org', 'msk', 'nn'] and mes not in ['1', '2']:
        return messages.get(key)[2]
    elif key == 'city':
        if mes == 'Москва':
            return messages.get(key)[0]
        elif mes == 'Нижний Новгород':
            return messages.get(key)[1]
        elif mes == 'error':
            return messages.get('cdek')[1]
        elif type(mes) is int:
            return '%s %s %s' % (messages.get('cdek')[0][0], mes, messages.get('cdek')[0][1])
    elif key == 'end':
        return messages.get('error')
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
    # status = sms.get_status(new_sms_id, num)


def get_answers(sms_id, phone, mes):

    client = session.query(Clients).filter(Clients.phone == phone).first()
    sent = session.query(Sent).filter(Sent.phone == phone).first()
    new_id, client_city = '', ''

    if sms_id == 'new':

        if mes.strip() == '1':

            new_id = 'city'
            sent.sms_id = new_id

        elif mes.strip() == '2':

            new_id = 'org'
            sent.sms_id = new_id

        else:

            new_id = 'end'
            sent.sms_id = new_id

    elif sms_id == 'city':

        client_city = mes.strip().title()
        print(client_city)
        
        if client_city == 'Москва':

            new_id = 'msk'
            sent.sms_id = new_id

        elif client_city == 'Нижний Новгород':

            new_id = 'nn'
            sent.sms_id = new_id

        else:
            price_cdek = cdek_delivery(client_city)
            print(price_cdek)

            if price_cdek in ('Empty', 'Overload', 'No delivery'):

                mes = 'error'
                new_id = 'end'
                sent.sms_id = new_id

            else:

                mes = price_cdek
                new_id = 'email'
                sent.sms_id = new_id

        client.city = client_city

    elif sms_id == 'org':

        if mes.strip() == '1':

            new_id = 'email'
            sent.sms_id = new_id

        elif mes.strip() == '2':
            new_id = 'end'
            sent.sms_id = new_id

        else:
            new_id = 'end'
            sent.sms_id = new_id

    elif sms_id == 'msk' or sms_id == 'nn':

        if mes.strip() == '1':

            new_id = 'address'
            sent.sms_id = new_id

        elif mes.strip() == '2':

            new_id = 'email'
            sent.sms_id = new_id

        else:
            
            new_id = 'end'
            sent.sms_id = new_id

    elif sms_id == 'address':

        new_id = 'end'
        sent.sms_id = new_id
        client.full_address = mes

    elif sms_id == 'email':

        new_id = 'fio'
        sent.sms_id = new_id
        client.email = mes

    elif sms_id == 'fio':
        
        new_id = 'end'
        sent.sms_id = new_id
        client.full_name = mes

    elif sms_id == 'end':
        new_id = 'end'
        sent.sms_id = new_id
        send_sms(phone, sms_id, new_id, 'error')
        return
        
    send_sms(phone, sms_id, new_id, mes)

    if new_id == 'end':

        if sms_id == 'address':
            email = TO_WHOM_EMAIL
            subject = 'Заказ с сайта на доставку по Москве или Нижнему Новгороду'
            message = '%s\n%s\n%s, %s' % (client.name, client.phone, client.city, client.full_address)
            send_attachment(email, subject, message)

        elif sms_id == 'fio':
            new_bill_contract = Bills(client_id=client.id)

            try:
                number = session.query(Bills.bill_num).filter(Bills.id == new_bill_contract.id - 1) + 1
            except:
                number = FIRST_NUMBER
            # ДОПИСАТЬ НАЗВАНИЕ ОШИБКИ
            
            file_path = get_bill(client.full_name, client.city, client.phone, number)
            subject = 'Счет на оплату ГП10МО'
            text = 'Добрый день!\nВаш счет!'
            send_attachment(client.email, subject, text, file_path)
            new_bill_contract.bill_num = number
            new_bill_contract.file_path = file_path
            session.add(new_bill_contract)
            session.commit()

    session.commit()