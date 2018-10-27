import requests
import zipfile
import io
import os
import shutil


def get_file(url):
    result = requests.get(url)
    file_zip = zipfile.ZipFile(io.BytesIO(result.content))
    folder = zipfile.ZipFile.namelist(file_zip)[0]

    new_path = os.getcwd()

    if os.path.exists(folder):
        shutil.rmtree(folder)

    if os.path.exists('CDEK_city.xls'):
        os.unlink('CDEK_city.xls')

    file_zip.extractall()

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if 'RUS' not in file_path:
            os.unlink(file_path)
        else:
            shutil.move(file_path, os.path.join(new_path, the_file))
            os.rename(os.path.join(new_path, the_file), os.path.join(new_path, 'CDEK_city.xls'))
    os.rmdir(folder)


if __name__ == '__main__':
    url = 'https://www.cdek.ru/website/edostavka/upload/custom/files/CDEK_city.zip'
    get_file(url)
