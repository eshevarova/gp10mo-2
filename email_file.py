import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
from project_files.mail_data import login as log
from project_files.mail_data import password as psw
from project_files.mail_data import smtpserver as smtp
from project_files.mail_data import from_address as fa
from project_files.mail_data import to_address as ta

logging.basicConfig(filename='attachment.log', level=logging.ERROR, format=' %(asctime)s - %(levelname)s - %(messages)s')


def send_attachment():
    from_address = fa  # от кого
    to_address = ta  # кому
    subject = 'Test email with attachment'  # тема письма
    login = log  # логин на сервере
    password = psw  # пароль
    smtpserver = smtp  # адрес smtp сервера

    message = MIMEMultipart()

    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject

    body = 'Проверка проверка проверка '  # email text

    message.attach(MIMEText(body, 'plain'))
    try:
        file_name = 'project_files/db_model.pdf'  # file path with extension

        with open(file_name, 'rb') as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= {}".format(file_name))
            message.attach(p)
    except FileNotFoundError as err:
        print(err)

    server = smtplib.SMTP(smtpserver)
    print(server.set_debuglevel(1))
    try:
        server.starttls()
        server.login(login, password)
        text = message.as_string()
        server.sendmail(from_address, to_address, text)
    except smtplib.SMTPHeloError as err1:
        logging.error(err1)
    except smtplib.SMTPAuthenticationError as err2:
        logging.error(err2)
    except smtplib.SMTPException as err3:
        logging.error(err3)
    finally:
        server.quit()


if __name__ == '__main__':
    send_attachment()
