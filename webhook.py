from flask import Flask, request, jsonify
import hashlib
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('leads-from-tg-697d5491301e.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('PS Store Requests')
sheet = spreadsheet.get_worksheet(0)

@app.route('/free-kassa-notification', methods=['POST'])
def free_kassa_notification():
    # sender_ip = request.remote_addr
    # if sender_ip not in FREEKASSA_IPS:
    #     return 'Forbidden', 403
    # else:
    secret_word_1 = ''  # Первое секретное слово
    secret_word_2 = ''  # Второе секретное слово
    merchant_id = 12345  # Номер вашего магазина
    order_id = request.form.get('MERCHANT_ORDER_ID')  # Номер заказа
    amount = request.form.get('AMOUNT')  # Сумма оплаты
    sign = request.form.get('SIGN')  # Подпись запроса

    # Генерируем подпись запроса
    sign_str = f'{merchant_id}:{amount}:{secret_word_1}:{order_id}:{secret_word_2}'
    sign_hash = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    # Проверяем правильность подписи
    if sign == sign_hash:
        # Подпись верна, обрабатываем оплату
        # Создаем клиент для работы с Google Sheets
  

        # Добавляем новую запись
        row = [order_id, amount, 'оплачен']
        sheet.append_row(row)

        # Возвращаем ответ FreeKassa
        return jsonify({'status': 'success'})
    else:
        # Подпись неверна, отклоняем оплату
        return jsonify({'status': 'error'})


@app.route('/free-kassa-notification', methods=['GET'])
def FKStatus():
    return 'Free-Kassa webhook is running'

@app.route('/', methods=['GET'])
def index():
    return 'Ну привет'

@app.route('/hehe', methods=['GET'])
def hehe():
    return 'hehe'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
