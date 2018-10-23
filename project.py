from flask import Flask, request, Response
from iteration_db_sms import add_to_db, first_sms
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

        if data['name']:
            name = data['name']
        else:
            return json.dumps({'status': 'Bad Request', 'code': 400})

        if data['tel']:
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
    if data['sms_id']:
        sms_id = data['sms_id']
    if data['mes']:
        message = data['mes']
    if data['phone']:
        client_tel = data['phone']
    return json.dumps({'status': 'Ok', 'code': 200})
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
