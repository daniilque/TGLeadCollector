import telebot
from flask import Flask, request, redirect
import hashlib
from flask_sslify import SSLify

bot = telebot.TeleBot('6066215488:AAEEzRgwqM-i2tbPqC_8u3skrOSU-U4lFi4')
app = Flask(__name__)



@app.route('/caba05a2af6d5d46ee7bc83959d06338', methods=['POST'])
def free_kassa_notification():
    data = request.form.to_dict()
    if data['m_operation_id'] and data['m_sign']:
        # Проверка подписи
        sign = data['m_sign']
        del data['m_sign']
        secret_key = "YOUR_FREE_KASSA_SECRET_KEY"
        check_sign = sorted(data.values()) + [secret_key]
        check_sign = "".join(check_sign).encode('utf-8')
        check_sign = hashlib.md5(check_sign).hexdigest()
        if sign == check_sign:
            # Подтверждение приема уведомления
            return 'YES'
        else:
            # Ошибка подписи
            return 'ERROR'
    else:
        # Ошибка в данных
        return 'ERROR'

@app.route('/', methods=['GET'])
def index():
    return 'Free-Kassa webhook is running'

@app.route('/hehe', methods=['GET'])
def hehe():
    return 'hehe'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)