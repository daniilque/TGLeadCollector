import telebot
from telebot import types
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Инициализация телеграм-бота
bot_token = '6004481628:AAFagZUopCcfTmGNB9y-JAcOSfOEnKFI6ZY'
bot = telebot.TeleBot(bot_token)

# Инициализация Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('leads-from-tg-697d5491301e.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('PS Store Requests')
sheet = spreadsheet.get_worksheet(0)
sheet_2 = spreadsheet.get_worksheet(2)

# Инициализация переменных
chat_status = ''
has_turkish_account = ''
turkish_account_login = 'Нет'
turkish_account_password = 'Нет'
user_choice = ''
sub_type = ''
price = ''
restart_msg = 'Напишите /restart, чтобы начать заново с выбора услуги или /start чтобы начать с указания аккаунта PS.'
log_pass_error = 'Неправильно введена связка логин:пароль'

# Маркер работы
print('Погнали')

# Забираем ласт номер таблы
# def get_last_result_num() -> int:
    
#     # Получение всех значений в столбце A
#     values_list = sheet.col_values(1)
    
#     # Удаление пустых значений
#     values_list = list(filter(None, values_list))
    
#     # Получение последнего номера результата
#     if not values_list:
#         last_result_num = 0
#     else:
#         last_result_num = int(values_list[-1])
    
#     return last_result_num

def get_last_result_num() -> int:
    last_result_num = sheet.cell(2,1).value
    return last_result_num

# Клавиатуры
def get_confirmation_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    confirm_button = types.KeyboardButton(text="Да")
    cancel_button = types.KeyboardButton(text="Отмена")
    keyboard.add(confirm_button, cancel_button)
    return keyboard

def get_cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cancel_button = types.KeyboardButton(text="Отмена")
    keyboard.add(cancel_button)
    return keyboard

def get_keyboard(buttons):
    keyboard = types.ReplyKeyboardMarkup(row_width=len(buttons))
    for button_text in buttons:
        button = types.KeyboardButton(button_text)
        keyboard.add(button)
    return keyboard

# def get_subList_keyboard(buttons):
#     keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     d1_button = types.KeyboardButton(text="Deluxe 1 месяц")
#     d3_button = types.KeyboardButton(text="Deluxe 3 месяца")
#     d12_button = types.KeyboardButton(text="Deluxe 12 месяцев")
#     x1_button = types.KeyboardButton(text="Deluxe 1 месяц")
#     x3_button = types.KeyboardButton(text="Deluxe 3 месяца")
#     x12_button = types.KeyboardButton(text="Deluxe 12 месяцев")
#     e1_button = types.KeyboardButton(text="Deluxe 1 месяц")
#     e3_button = types.KeyboardButton(text="Deluxe 3 месяца")
#     e12_button = types.KeyboardButton(text="Deluxe 12 месяцев")
#     keyboard.add(cancel_button)
#     return keyboard

def get_subList_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    d_button = types.KeyboardButton(text="Deluxe")
    x_button = types.KeyboardButton(text="Extra")
    e_button = types.KeyboardButton(text="Essential")
    keyboard.add(d_button, x_button, e_button)
    return keyboard

def get_subLen_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    _1_button = types.KeyboardButton(text="1 месяц")
    _3_button = types.KeyboardButton(text="3 месяца")
    _12_button = types.KeyboardButton(text="12 месяцев")
    keyboard.add(_1_button, _3_button, _12_button)
    return keyboard


# Функция для отправки сообщения в чат с id=-1001830767950
def send_notification(message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    #params = {'chat_id': '-1001830767950', 'text': message} 
    params = {'chat_id': '5663237104', 'text': message}
    requests.post(url, json=params)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global chat_status, turkish_account_login, turkish_account_password
    chat_status = 'started'
    turkish_account_login = 'Нет'
    turkish_account_password = 'Нет'
    bot.send_message(message.chat.id, 'Здравствуйте! Есть ли у вас турецкий аккаунт PS Store?', reply_markup=get_keyboard(['Да', 'Нет']))

# Обработчик отмены заказа
@bot.message_handler(func=lambda message: chat_status in ['has_turkish_account', 'user_choice', 'order_confirmation', 'game_confirmation'] and message.text == 'Отмена')
def cancel_order_message(message):
    global chat_status
    chat_status = ''
    bot.send_message(message.chat.id, f"Заказ отменен. {restart_msg}")

# Обработчик ответа на вопрос о наличии аккаунта
@bot.message_handler(func=lambda message: chat_status == 'started' and message.text == 'Да')
def has_turkish_account_message(message):
    global chat_status, has_turkish_account
    chat_status = 'has_turkish_account'
    has_turkish_account = message.text
    bot.send_message(message.chat.id, 'Отлично, тогда напишите, пожалуйста, свой логин и пароль от турецкого аккаунта в формате "email_адрес:пароль", чтобы мы могли проверить наличие подходящих игр и подписок.', reply_markup=get_cancel_keyboard())

# Обработчик ответа на вопрос о логине и пароле от аккаунта
# @bot.message_handler(commands=['restart'])
# @bot.message_handler(func=lambda message: chat_status == 'has_turkish_account' or chat_status == 'started' and message.text == 'Нет')
# def turkish_account_credentials_message(message):
#     global chat_status, turkish_account_login, turkish_account_password
#     if has_turkish_account == 'Да' and chat_status == 'has_turkish_account': 
#         while True:
#             try: 
#                 turkish_account_login, turkish_account_password = message.text.split(':')
#                 break
#             except: 
#                 bot.send_message(message.chat.id, log_pass_error)
#             break

#     chat_status = 'user_choice'
#     bot.send_message(message.chat.id, 'Что вас интересует - игра или подписка?', reply_markup=get_keyboard(['Игра', 'Подписка']))

@bot.message_handler(commands=['restart'])
@bot.message_handler(func=lambda message: chat_status == 'has_turkish_account' or chat_status == 'started' and message.text == 'Нет')
def turkish_account_credentials_message(message):
    global chat_status, turkish_account_login, turkish_account_password
    if has_turkish_account == 'Да' and chat_status == 'has_turkish_account': 
        # bot.send_message(message.chat.id, 'Введите логин и пароль через двоеточие, например: login:password')
        get_turkish_account_credentials(message)
    else:
        chat_status = 'user_choice'
        bot.send_message(message.chat.id, 'Что вас интересует - игра или подписка?', reply_markup=get_keyboard(['Игра', 'Подписка']))


def get_turkish_account_credentials(message):
    global chat_status, turkish_account_login, turkish_account_password
    try: 
        turkish_account_login, turkish_account_password = message.text.split(':')
        chat_status = 'user_choice'
        bot.send_message(message.chat.id, 'Что вас интересует - игра или подписка?', reply_markup=get_keyboard(['Игра', 'Подписка']))
    except: 
        bot.send_message(message.chat.id, log_pass_error)
        bot.register_next_step_handler(message, get_turkish_account_credentials)
    

# # Обработчик ответа на вопрос о выборе пользователя
# @bot.message_handler(func=lambda message: chat_status == 'user_choice' and message.text == 'Подписка')
# def user_choice_message(message):
#     global chat_status, user_choice, sub_type, price
#     chat_status = 'order_confirmation'
#     user_choice = message.text    
#     sub_type = 'Deluxe 12 месяцев'
#     cell = sheet_2.find(sub_type)
#     row_number = cell.row
#     price = sheet_2.cell(row_number, 2).value
#     price = sheet.cell(2, 2).value
#     bot.send_message(message.chat.id, f"Вы выбрали подписку {sub_type} за {price}₺. Хотите подтвердить заказ?", reply_markup=get_confirmation_keyboard())

 # Обработчик ответа выбора подписки
@bot.message_handler(func=lambda message: chat_status == 'user_choice' and message.text == 'Подписка')
def user_choice_message(message):
    global chat_status, user_choice
    chat_status = 'sub_type_choise'
    user_choice = 'Подписка'   
    bot.send_message(message.chat.id, "Какой тип подписки вас интересует?", reply_markup=get_subList_keyboard()) 

# Обработчик выбора длинны подписки
@bot.message_handler(func=lambda message: chat_status == 'sub_type_choise')
def user_choice_message(message):
    global chat_status, sub_cat, sub_len
    sub_cat = message.text
    chat_status = 'sub_len_choise'    
    bot.send_message(message.chat.id, "На какой срок?", reply_markup=get_subLen_keyboard())

# Обработчик ответа на вопрос о выборе пользователя
@bot.message_handler(func=lambda message: chat_status == 'sub_len_choise')
def user_choice_message(message):
    global chat_status, sub_type, price
    sub_len = message.text
    chat_status = 'order_confirmation' 
    sub_type = sub_cat + ' ' + sub_len
    print(sub_type)
    cell = sheet_2.find(sub_type)
    row_number = cell.row
    price = sheet_2.cell(row_number, 2).value

    bot.send_message(message.chat.id, f"Вы выбрали подписку {sub_type} за {price}₺. Хотите подтвердить заказ?", reply_markup=get_confirmation_keyboard())
 

# # Обработчик ответа на вопрос об игре
# @bot.message_handler(func=lambda message: chat_status == 'user_choice' and message.text == 'Игра')
# def game_choice_message(message):
#     global chat_status, price
#     chat_status = 'game_confirmation'
#     price = sheet.cell(2, 2).value
#     bot.send_message(message.chat.id, "Введите название игры на английском языке", reply_markup=get_cancel_keyboard())

# # Обработчик ответа на вопрос о названии игры
# @bot.message_handler(func=lambda message: chat_status == 'game_confirmation')
# def game_confirmation_message(message):
#     global chat_status, game_name
#     game_name = message.text
#     bot.send_message(message.chat.id, f"Вы выбрали игру {game_name} за {price}₺. Хотите подтвердить заказ?", reply_markup=get_confirmation_keyboard())

# Обработчик ответа на вопрос об игре
@bot.message_handler(func=lambda message: chat_status == 'user_choice' and message.text == 'Игра')
def game_choice_message(message):
    global chat_status
    chat_status = 'game_confirmation'
    bot.send_message(message.chat.id, f'Продажа игр происходит по следующему курсу:\n5₽ за 1₺ при покупке до 500₺\n4,8₽ за 1₺ при покупке от 500₺ до 1000₺\n4,5₽ за 1₺ при покупке от 1000₺\nТак как я пока не умею распознавать названия игр, перевожу тебя на живого человека', reply_markup=get_confirmation_keyboard())

# Обработчик подтверждения заказа
@bot.message_handler(func=lambda message: chat_status in ['order_confirmation', 'game_confirmation'] and message.text == 'Да')
def confirm_order_message(message):
    global chat_status
    chat_status = 'order_confirmed'
    last_result_num = get_last_result_num()
    order_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    user_final_choise = sub_type if user_choice == 'Подписка' else 'Игра'#game_name
    sheet.insert_row([int(last_result_num) + 1, message.chat.id, message.chat.username, turkish_account_login, turkish_account_password, user_final_choise, price, order_time], 2)
    bot.send_message(message.chat.id, f"Спасибо за заказ! Мы свяжемся с вами в ближайшее время для оформления покупки. {restart_msg}")
    send_notification(f"Новый заказ!\nВремя заказа: {order_time}\nChat ID: {message.chat.id}\nНаличие турецкого аккаунта: {has_turkish_account}\nЛогин от турецкого аккаунта: {turkish_account_login}\nВыбор пользователя: {user_choice}\nНазвание: {user_final_choise}\nЦена: {price}₺")


# Запуск бота
bot.polling(none_stop=True)
