from flask import Flask, request, Response

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
            return json.dumps({'status': 'fail', 'message': 'Empty value of name'})
        if data['tel']:
            tel = data['tel']
        else:
            return json.dumps({'status': 'fail', 'message': 'Empty value of tel'})
        with open('clients.txt', 'a', encoding='utf-8') as f:
            f.write("%s %s\n" % (name, tel))
        return json.dumps({'status': 'ok', 'message': 'We got your request'})
    else:
        return 'Do not use GET, use POST'


@app.route("/sms", methods = ['POST'])
def get_sms_data():
    data = request.get_json()
    if data['sms_id']:
        sms_id = data['sms_id']
    if data['mes']:
        message = data['mes']
    if data['phone']:
        client_tel = data['phone']
    return json.dumps({'status': 'ok'})
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
