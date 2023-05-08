import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import telebot
from telebot import types
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


# Инициализация телеграм-бота
bot_token = 'token'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Инициализация Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('leads-from-tg-697d5491301e.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('PS Store Requests')
sheet = spreadsheet.get_worksheet(0)
sheet_1 = spreadsheet.get_worksheet(1)
sheet_2 = spreadsheet.get_worksheet(2)


# Инициализация переменных
chat_status = ''
orders_list = []
has_turkish_account = ''
turkish_account_login = 'Нет'
turkish_account_password = 'Нет'
user_choice = ''
sub_type = ''
price = ''
restart_msg = 'Напишите /restart, чтобы начать заново с выбора услуги или /start чтобы начать с указания аккаунта PS.'
log_pass_error = 'Неправильно введена связка логин:пароль'
price_error = 'Неправильно введена стоимость игры в лирах'

# Маркер работы
print('Погнали')


# Последняя цифра заказа
def get_last_result_num() -> int:
    last_result_num = sheet.cell(2,1).value
    return last_result_num

# Актуальный курс
def get_ex_rate() -> float:
    ex_rate = sheet_1.cell(1,2).value
    return ex_rate


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
    keyboard = types.ReplyKeyboardMarkup(row_width=len(buttons), resize_keyboard=True)
    for button_text in buttons:
        button = types.KeyboardButton(button_text)
        keyboard.add(button)
    return keyboard

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


# Создаем объект клавиатуры
urlkb = types.InlineKeyboardMarkup()

# # Создаем кнопки со ссылками
# urlkb.add(types.InlineKeyboardButton(text='Наша страница на Авито', url='https://www.avito.ru/voronezh/igry_pristavki_i_programmy/ps_plyus_turtsiya_2909166258'))
# urlkb.add(types.InlineKeyboardButton(text='Наша страница на Авито №2', url='https://www.avito.ru/novosibirsk/igry_pristavki_i_programmy/podpiska_ps_plus_2908872126'))
urlkb.add(types.InlineKeyboardButton(text='Наш Instagram Аккаунт', url='https://www.instagram.com/turk_sub_store/'))
urlkb.add(types.InlineKeyboardButton(text='Связаться с администратором', url='https://t.me/plusturkadmin/'))



# Функция для отправки сообщения в чат с id=-1001830767950
def send_notification(message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    global manager_chatid
    #manager_chatid = -1001830767950
    manager_chatid = 5663237104
    params = {'chat_id': manager_chatid, 'text': message}
    requests.post(url, json=params)

# Проверка юзера по базе
def check_orders(message):
    orders = []
    orders_done = 0
    chat_id = message.chat.id
    user_id = message.chat.username
    for i in range(2, sheet.row_count):
        if sheet.cell(i, 2).value == str(chat_id) or sheet.cell(i, 3).value == str(user_id):
            order_date = sheet.cell(i, 10).value
            order_status = sheet.cell(i, 11).value
            if order_status == 'В работе':
                order_info = sheet.cell(i, 8).value
                orders.append((order_date, order_info))
            else:
                orders_done +=1
    return orders, orders_done

    
# Вывод заказов
def send_orders(orders, orders_done, chat_id):
    for order in orders:
        order_date = order[0]
        order_info = order[1]
        message_text = "Заказ от {} :\n{}".format(order_date, order_info)
        bot.send_message(chat_id, message_text)
    bot.send_message(chat_id, f'Завершенных заказов на этой неделе: {orders_done}')

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_message(message):
    global chat_status, turkish_account_login, turkish_account_password
    chat_status = 'started'
    turkish_account_login = 'Нет'
    turkish_account_password = 'Нет'
    orders_list, orders_done = check_orders(message)
    if orders_list or orders_done:
        chat_status = 'has_turkish_account'
        bot.send_message(message.chat.id, f'Здравствуйте, {message.chat.username}! Ваши активные заказы:', reply_markup=get_keyboard(['Продолжить']))
        send_orders(orders_list, orders_done, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Здравствуйте! Есть ли у вас турецкий аккаунт PS Store?', reply_markup=get_keyboard(['Да', 'Нет', 'Наши ссылки']))

# Обработчик отмены заказа
@dp.message_handler(func=lambda message: message.text == 'Отмена')
async def cancel_order_message(message):
    global chat_status
    chat_status = ''
    bot.send_message(message.chat.id, f"Заказ отменен. {restart_msg}")

# Обработчик ответа на вопрос о наличии аккаунта
@dp.message_handler(func=lambda message: chat_status == 'started' and message.text == 'Да')
async def has_turkish_account_message(message):
    global chat_status, has_turkish_account
    chat_status = 'has_turkish_account'
    has_turkish_account = message.text
    bot.send_message(message.chat.id, 'Отлично, тогда напишите, пожалуйста, свой логин и пароль от турецкого аккаунта в формате "email_адрес:пароль", чтобы мы могли проверить наличие подходящих игр и подписок.', reply_markup=get_cancel_keyboard())

@dp.message_handler(commands=['restart'])
@dp.message_handler(func=lambda message: chat_status == 'has_turkish_account' or chat_status == 'started' and message.text == 'Нет')
async def turkish_account_credentials_message(message):
    global chat_status, turkish_account_login, turkish_account_password
    if has_turkish_account == 'Да' and chat_status == 'has_turkish_account': 
        get_turkish_account_credentials(message)
    else:
        chat_status = 'user_choice'
        bot.send_message(message.chat.id, 'Что вас интересует - игра или подписка?', reply_markup=get_keyboard(['Игра', 'Подписка', 'Наши ссылки']))


async def get_turkish_account_credentials(message):
    global chat_status, turkish_account_login, turkish_account_password
    try: 
        turkish_account_login, turkish_account_password = message.text.split(':')
        chat_status = 'user_choice'
        bot.send_message(message.chat.id, 'Что вас интересует - игра или подписка?', reply_markup=get_keyboard(['Игра', 'Подписка']))
    except: 
        bot.send_message(message.chat.id, log_pass_error)
        bot.register_next_step_handler(message, get_turkish_account_credentials)
    
 # Обработчик ответа выбора подписки
@dp.message_handler(func=lambda message: chat_status == 'user_choice' and message.text == 'Подписка')
async def user_choice_message(message):
    global chat_status, user_choice
    chat_status = 'sub_type_choise'
    user_choice = 'Подписка'   
    bot.send_message(message.chat.id, "Какой тип подписки вас интересует?", reply_markup=get_subList_keyboard()) 

# Обработчик выбора срока подписки
@dp.message_handler(func=lambda message: chat_status == 'sub_type_choise')
async def user_choice_message(message):
    global chat_status, sub_cat, sub_len
    sub_cat = message.text
    chat_status = 'sub_len_choise'    
    bot.send_message(message.chat.id, "На какой срок?", reply_markup=get_subLen_keyboard())

# Обработчик ответа на вопрос о выборе пользователя
@dp.message_handler(func=lambda message: chat_status == 'sub_len_choise')
async def user_choice_message(message):
    global chat_status, sub_type, sub_price
    sub_len = message.text
    chat_status = 'order_confirmation' 
    sub_type = sub_cat + ' ' + sub_len
    cell = sheet_2.find(sub_type)
    row_number = cell.row
    sub_price = sheet_2.cell(row_number, 2).value

    bot.send_message(message.chat.id, f"Вы выбрали подписку {sub_type} за {sub_price}р. Хотите подтвердить заказ?", reply_markup=get_confirmation_keyboard())
    
 
# Обработчик ответа на вопрос об игре
@dp.message_handler(func=lambda message: chat_status == 'user_choice' and message.text == 'Игра')
async def game_choice_message(message):
    global chat_status, user_choice
    chat_status = 'game_info'
    user_choice = 'Игра'
    bot.send_message(message.chat.id, f'Продажа игр происходит по следующему курсу:\n5₽ за 1₺ при покупке до 500₺\n4,8₽ за 1₺ при покупке от 500₺ до 1000₺\n4,5₽ за 1₺ при покупке от 1000₺\n\nПосле оплаты вы получите данные одноразовой виртуальной карты номиналом на указанную стоимость.\nНеобходимо использовать эту карту для проведения одного платежа на всю сумму, так как неиспользованные деньги на балансе карты сгорают после одной оплаты.\nК сожалению этот метод не работает с подписками\n\nВведите стоимость игры в лирах (только цифры)', reply_markup=get_cancel_keyboard())

# Обработчик стоимости игры
@dp.message_handler(lambda message: chat_status == 'game_info')
async def game_choice_message(message: types.Message):
    global chat_status, user_choice, price, price_rub
    chat_status = 'game_confirmation'
    try:
        price = int(message.text)
        if price <= 500:
            price_rub = price * 5
        elif price <= 1000:
            price_rub = price * 4.8
        else:
            price_rub = price * 4.5
        await bot.send_message(
            message.chat.id,
            f'Стоимость игры: {round(price_rub, 2)} рублей. Хотите подтвердить заказ?',
            reply_markup=get_keyboard(['Да', 'Указать другую сумму', 'Отмена'])
        )
    except ValueError:
        await bot.send_message(message.chat.id, price_error)
        await game_choice_message(message)


@dp.message_handler(lambda message: chat_status == 'game_confirmation')
async def game_confirmation(message: types.Message):
    if message.text == 'Да':
        await confirm_order_message(message)
    elif message.text == 'Указать другую сумму':
        # возвращаем пользователя на предыдущий шаг
        chat_status = 'game_info'
        await bot.send_message(message.chat.id, 'Введите другую сумму')
        await game_choice_message(message)


# Обработчик подтверждения заказа
@dp.message_handler(lambda message: message.text == 'Да' and chat_status in ['order_confirmation', 'game_confirmation'])
async def confirm_order_message(message: types.Message):
    global chat_status
    a_username = message.chat.username
    chat_status = 'order_confirmed'
    last_result_num = get_last_result_num()
    order_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if user_choice == 'Подписка':
        user_final_choice = sub_type
        price = sub_price
    else:
        user_final_choice = user_choice
        price = price_rub
    try:
        name_surname = message.chat.first_name + ' ' + message.chat.last_name
    except TypeError:
        try:
            name_surname = message.chat.first_name
        except TypeError:
            name_surname = 'Null'
    try:
        contact = message.contact.phone_number
    except AttributeError:
        contact = 'Null'
    print(user_choice)
    sheet.insert_row([
        int(last_result_num) + 1,
        message.chat.id,
        a_username,
        name_surname,
        contact,
        turkish_account_login,
        turkish_account_password,
        user_final_choice,
        price,
        order_time,
        'В работе',
    ], 2)

    await bot.send_message(message.chat.id, f"Спасибо за заказ!\n{restart_msg}")
    send_notification(
        f"Новый заказ!\n"
        f"Время заказа: {order_time}\n"
        f"Chat ID: {message.chat.id}\n"
        f"Login: @{a_username}\n"
        f"Наличие турецкого аккаунта: {has_turkish_account}\n"
        f"Логин от турецкого аккаунта: {turkish_account_login}\n"
        f"Выбор пользователя: {user_choice}\n"
        f"Название: {user_final_choice}\n"
        f"Цена: {price}₺"
        )
    await bot.forward_message(manager_chatid, from_chat_id=message.chat.id, message_id=message.message_id) 

@dp.message_handler(func=lambda message: message.text == 'Наши ссылки')
async def urls(message):
    bot.send_message(message.chat.id, 'Полезные ссылки:', reply_markup=urlkb)

# Запуск бота
bot.polling(none_stop=True)
