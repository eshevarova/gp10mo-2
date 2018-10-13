import xlrd
import os

def get_id(city):
    filename = 'CDEK_city.xls'
    file_path = os.path.join(os.getcwd(), filename)

    work_book = xlrd.open_workbook(file_path)
    work_sheet = work_book.sheet_by_index(0)

    names_num = 0
    for row in range(1, work_sheet.nrows):
        if isinstance(work_sheet.cell_value(row, 2), str):
            if city == work_sheet.cell_value(row, 2).split(', ')[0]:
                names_num += 1
                city_id = work_sheet.cell_value(row, 0)
            else:
                continue
    if names_num == 0:
        return 'Empty'
    elif names_num == 1:
        return str(int(city_id))
    elif names_num > 1:
        return 'Overload'


if __name__ == "__main__":
    print(get_id('Москва'))