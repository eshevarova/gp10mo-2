import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os.path import basename
import logging
from project_files.parameters import FROM_WHOM_EMAIL, LOGIN_EMAIL, \
                                        PASSWORD_EMAIL, SMTPSERVER


logging.basicConfig(filename='attachment.log', level=logging.ERROR, format=' %(asctime)s - %(levelname)s - %(messages)s')


def send_attachment(email, subject, text, file_path=None):
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
            p = MIMEApplication(attachment.read(), Name=basename(file_path))

        p['Content-Disposition'] = 'attachment; filename= {}'.format(basename(file_path))
        message.attach(p)
    except FileNotFoundError as err:
        print(err)
    except TypeError:
        pass

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

if __name__ == '__main__':
    send_attachment('kat121193@yandex.ru', 'Счет', 'Приветик', 'bills/Schet_na_oplatu_18769_от_06.11.2018.xls')