from xlrd import open_workbook
import xlwt
import os
from datetime import datetime, timedelta
from xlutils.copy import copy

"""
обязательно перед запуском создать директорию bills
"""

def get_bill(full_name, city, tel):

    with open('num.txt', 'r', encoding='utf-8') as f:
        num = f.read()

    with open('num.txt', 'w', encoding='utf-8') as f:
        new_num = str(int(num) + 1)
        f.write(new_num)

    filename = 'Schet_na_oplatu.xls'
    file_path = os.path.join(os.getcwd(), filename)

    rb = open_workbook(file_path, formatting_info=True)
    r_sheet = rb.sheet_by_index(0)

    wb = copy(rb)
    w_sheet = wb.get_sheet(0)

    date_now = datetime.now().strftime('%d.%m.%Y')
    delta = timedelta(days=3)

    num_and_date = 'Счет-договор на оплату № %s от %s' % (num, date_now)
    client_data = '%s, г. %s, тел.: %s' % (full_name, city, tel)
    date_pay = (datetime.strptime(date_now, '%d.%m.%Y') + delta).date().strftime('%d.%m.%Y')
    latest_pay = 'Оплатить не позднее %s' % (date_pay)
    
    new_filename = 'Schet_na_oplatu_%s_от_%s.xls' % (num, date_now)
    new_path = os.path.join(os.getcwd(), 'bills')
    new_path = os.path.join(new_path, new_filename)

    w_sheet.write(9, 1, num_and_date)
    w_sheet.write(16, 6, client_data)
    w_sheet.write(19, 6, num_and_date)
    w_sheet.write(30, 1, latest_pay)


    wb.save(new_path)

    return new_path

print(get_bill('Шеварова Екатерина Алексеевна', 'Москва', '79165235185'))