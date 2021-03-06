from xlrd import open_workbook
import xlwt
import os
from datetime import datetime, timedelta
from xlutils.copy import copy
from project_files.parameters import BILLS_FOLDER, BILL_FILENAME

def get_bill(full_name, city, tel, number):

    file_path = os.path.join(os.getcwd(), BILL_FILENAME)

    rb = open_workbook(file_path, formatting_info=True)
    r_sheet = rb.sheet_by_index(0)

    wb = copy(rb)
    w_sheet = wb.get_sheet(0)

    date_now = datetime.now()
    delta = timedelta(days=3)

    num_and_date = 'Счет-договор на оплату № %s от %s' % (number, date_now.strftime('%d.%m.%Y'))
    client_data = '%s, г. %s, тел.: %s' % (full_name, city, tel)
    date_pay = date_now + delta
    latest_pay = 'Оплатить не позднее %s' % (date_pay.strftime('%d.%m.%Y'))
    
    new_filename = 'Schet_na_oplatu_%s_от_%s.xls' % (number, date_now.strftime('%d.%m.%Y'))
    new_path = os.path.join(os.getcwd(), BILLS_FOLDER)
    new_path = os.path.join(new_path, new_filename)
    path_to_attach = os.path.join(BILLS_FOLDER, new_filename)

    w_sheet.write(9, 1, num_and_date)
    w_sheet.write(16, 6, client_data)
    w_sheet.write(19, 6, num_and_date)
    w_sheet.write(30, 1, latest_pay)


    wb.save(new_path)
    return path_to_attach