"""
send email with Python
"""

import smtplib
from email.mime.text import MIMEText
import logging
import netrc

logging.basicConfig(filename='email.log', level=logging.ERROR, format=' %(asctime)s - %(levelname)s - %(messages)s')


def sendmail(email):
    """
    Отправка сообщения
    :return:
    """
    from_address = ''  # от кого
    to_address = email  # кому
    subject = ''  # тема письма
    login = ''  # логин на сервере
    password = ''  # пароль
    smtpserver = ''  # адрес smtp сервера

    message = " "  # текст сообщения
    message = MIMEText(message, 'plain', 'utf-8')  # кодировка

    mail_body = '\r\n'.join((
        'From: {}'.format(from_address),
        'To: {}'.format(to_address),
        'Subject: {}'.format(subject),
        message.as_string()  # конвертация в строку
    ))

    server = smtplib.SMTP(smtpserver)
    server.set_debuglevel(1)

    try:
        server.starttls()
        server.login(login, password)
        server.sendmail(from_address, to_address, mail_body)
    except smtplib.SMTPHeloError as err1:
        print(err1)
    except smtplib.SMTPAuthenticationError as err2:
        print(err2)
    except smtplib.SMTPException as err3:
        print(err3)
    finally:
        server.quit()

