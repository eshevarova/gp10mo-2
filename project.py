from flask import Flask, request, Response
from iteration_db_sms import add_to_db, first_sms, db_check_date, sms_message, send_sms, get_answers
from clean_phone import clean_user_phone
import json


app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello!'


@app.route("/clients", methods =['POST', 'GET'])
def get_client_data():
    if request.method == 'POST':
        data = request.get_json()

        if data.get('name', 0):
            name = data['name']
        else:
            return json.dumps({'status': 'Bad Request', 'code': 400})

        if data.get('tel', 0):
            tel = data['tel']
        else:
            return json.dumps({'status': 'Bad Request', 'code': 400})

        tel = clean_user_phone(tel)

        add_to_db(tel, name)

        if name.lower() in ['test', 'тест']:
            first_sms(tel)

        return json.dumps({'status': 'Ok', 'code': 200})
    else:
        return json.dumps({'status': 'Method Not Allowed', 'code': 405})


@app.route("/sms", methods = ['POST'])
def get_sms_data():
    data = request.get_json()

    if data.get('sms_id', 0):
        sms_id = data['sms_id']
    else:
        return json.dumps({'status': 'Bad Request', 'code': 400})

    if data.get('mes', 0):
        message = data['mes']
    else:
        return json.dumps({'status': 'Bad Request', 'code': 400})

    if data.get('phone', 0):
        client_tel = data['phone']
    else:
        return json.dumps({'status': 'Bad Request', 'code': 400})

    get_answers(sms_id, client_tel, message)

    return json.dumps({'status': 'Ok', 'code': 200})
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
