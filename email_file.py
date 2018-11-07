import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
from project_files.mail_parameters import *


logging.basicConfig(filename='attachment.log', level=logging.ERROR, format=' %(asctime)s - %(levelname)s - %(messages)s')


def send_attachment(email, subject, text, file_path):
    from_address = FROM_WHOM_EMAIL  # от кого
    login = LOGIN_EMAIL  # логин на сервере
    password = PASSWORD_EMAIL  # пароль
    smtpserver = SMTPSERVER  # адрес smtp сервера

    message = MIMEMultipart()

    message['From'] = from_address
    message['To'] = email
    message['Subject'] = subject

    message.attach(MIMEText(text, 'plain', 'utf-8'))
    try:
        with open(file_path, 'rb') as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= {}".format(file_path))
            message.attach(p)
    except FileNotFoundError as err:
        print(err)

    server = smtplib.SMTP(smtpserver)
    print(server.set_debuglevel(1))
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
