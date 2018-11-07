import requests
from project_files.service_access import *
from db import Clients, session, Sent, Received, Bills

last_row = session.query(Received).order_by(Received.input_id.desc()).first()
after_id = last_row.input_id
url = 'https://smsc.ru/sys/get.php?get_answers=1&login=%s&psw=%s&fmt=3&hour=1&after_id=%s' % (LOGIN_SMS, PASSWORD_SMS, after_id)

def get_input_sms(url):
    return requests.get(url).json()


def key_date(json_dict):
    return json_dict['sent']

data = get_input_sms(url)
sorted_data = sorted(data, key=key_date)


phone, message, input_id, used_phones = '', '', '', []

for dict_elem in sorted_data:
    phone = '+%s' % dict_elem['phone']
    message = dict_elem['message']
    input_id = dict_elem['id']

    client = session.query(Clients).filter(Clients.phone == phone).first()
    sent = session.query(Sent).filter(Sent.phone == phone).first()

    answer = Received(sms_id=sent.sms_id, phone=phone, mes=message, input_id=input_id)
    session.add(answer)
    session.commit()





    if phone in used_phones:
        continue
