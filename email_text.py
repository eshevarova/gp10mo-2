"""
send email with Python
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from project_files.mail_parameters import *
import logging

logging.basicConfig(filename='email.log', level=logging.ERROR, format=' %(asctime)s - %(levelname)s - %(messages)s')


def sendmail(email, subject, message):
    from_address = FROM_WHOM_EMAIL  # от кого
    login = LOGIN_EMAIL  # логин на сервере
    password = PASSWORD_EMAIL  # пароль
    smtpserver = SMTPSERVER  # адрес smtp сервера

    message = MIMEText(message, 'plain', 'utf-8')  # кодировка
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = from_address
    message['To'] = email


    server = smtplib.SMTP(smtpserver)
    server.set_debuglevel(1)

    try:
        server.starttls()
        server.login(login, password)
        server.sendmail(from_address, email, message.as_string())
    except smtplib.SMTPHeloError as err1:
        logging.error(err1)
    except smtplib.SMTPAuthenticationError as err2:
        logging.error(err2)
    except smtplib.SMTPException as err3:
        logging.error(err3)
    finally:
        server.quit()
