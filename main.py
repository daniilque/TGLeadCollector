from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import gspread
from oauth2client.service_account import ServiceAccountCredentials


API_TOKEN_TG = '6066215488:AAGXJP8pJ6WpA3i0tCgYKKdloDPi4QC_Cyw'
bot = Bot(token=API_TOKEN_TG)
dp = Dispatcher(bot)
messageNumber = 0

# define the credentials for accessing the Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('leads-from-tg-697d5491301e.json', scope)
client = gspread.authorize(creds)

# open the Google Sheet
sheet = client.open('PS Store Requests').sheet1




urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Наша страница на Авито', url='https://www.avito.ru/sankt-peterburg/igry_pristavki_i_programmy/igry_podpiska_playstation_plus_turtsiya_2906755318')
urlButton2 = InlineKeyboardButton(text='Наша страница на Авито №2', url='https://www.avito.ru/voronezh/igry_pristavki_i_programmy/podpiska_playstation_plus_1_3_12_mesyatsev_2825626676')
urlButton3 = InlineKeyboardButton(text='Наш Instagram Аккаунт', url='https://www.instagram.com/tr_playstation_store/')
urlkb.add(urlButton,urlButton2,urlButton3)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="Есть"),
           types.KeyboardButton(text="Нет"),
           types.KeyboardButton(text="Наши страницы")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Привет!\nЯ Бот, который поможет тебе определиться с покупкой!\nДля начала, скажи, есть ли у тебя турецкий аккаунт в PS Store:", reply_markup=keyboard)



@dp.message_handler(lambda message: message.text == "Есть" or message.text == "Нет" or message.text == "К выбору услуг")
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="Подписки"),
           types.KeyboardButton(text="Игры"),
           types.KeyboardButton(text="Наши страницы")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Что тебя интересует?", reply_markup=keyboard)
   if message.text != 'К выбору услуг':
    global messageAccount
    messageAccount = message.text


@dp.message_handler(lambda message: message.text == "Игры")
async def handle_keyboard_message(message: types.Message):
    kb = [
       [
           types.KeyboardButton(text="Подтвердить")
       ],
   ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
    user_username = message.from_user.username
    await bot.send_message(chat_id='119485896', text=f'Поступил запрос на игру от пользователя @{user_username}')
    await bot.send_message(chat_id=message.chat.id, text=f'Продажа игр происходит по следующему курсу:\n5₽ за 1₺ при покупке до 500₺\n4,8₽ за 1₺ при покупке от 500₺ до 1000₺\n4,5₽ за 1₺ при покупке от 1000₺\n Так как я пока не умею распознавать названия игр, перевожу тебя на живого человека', reply_markup=keyboard)
    global messageService
    messageService = message.text
    

@dp.message_handler(lambda message: message.text == "Подписки")
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="PS Plus Deluxe"),
           types.KeyboardButton(text="PS Plus Extra"),
           types.KeyboardButton(text="PS Plus Essential"),
           types.KeyboardButton(text="К выбору услуг")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Какую версию подписки?", reply_markup=keyboard)
   
@dp.message_handler(lambda message: message.text == "PS Plus Deluxe")
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="DELUXE 1 месяц"),
           types.KeyboardButton(text="DELUXE 3 месяца"),
           types.KeyboardButton(text="DELUXE 12 месяцев"),
           types.KeyboardButton(text="К выбору услуг")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Какую версию подписки?", reply_markup=keyboard)
   global messageService
   messageService = message.text

@dp.message_handler(lambda message: message.text == "PS Plus Essential")
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="Essential 1 месяц"),
           types.KeyboardButton(text="Essential 3 месяца"),
           types.KeyboardButton(text="Essential 12 месяцев"),
           types.KeyboardButton(text="К выбору услуг")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Какую версию подписки?", reply_markup=keyboard)
   global messageService
   messageService = message.text

@dp.message_handler(lambda message: message.text == "PS Plus Extra")
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="Extra 1 месяц"),
           types.KeyboardButton(text="Extra 3 месяца"),
           types.KeyboardButton(text="Extra 12 месяцев"),
           types.KeyboardButton(text="К выбору услуг")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Какую версию подписки?", reply_markup=keyboard)
   global messageService
   messageService = message.text

@dp.message_handler(lambda message: message.text == "Подтвердить")
async def send_welcome(message: types.Message):
   global messageService
   global messageNumber
   messageNumber = messageNumber + 1
   row = [messageNumber, message.chat.id, message.chat.username, messageAccount, messageService]
   sheet.append_row(row)
   kb = [
       [
           types.KeyboardButton(text="К выбору услуг")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Спасибо за заказ! \nИнформация передана администратору, скоро он с вами свяжется для осуществления сделки", reply_markup=keyboard)
   messageService = message.text

@dp.message_handler(lambda message: message.text == "Игры")
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="К выбору услуг")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Продажа игр происходит по следующему курсу:\n5₽ за 1₺ при покупке до 500₺\n4,8₽ за 1₺ при покупке от 500₺ до 1000₺\n4,5₽ за 1₺ при покупке от 1000₺\n Так как я пока не умею распознавать названия игр, перевожу тебя на живого человека", reply_markup=keyboard)


# @dp.message_handler(lambda message: message.text == "Игры") 
# async def echo(message: types.Message): 
#    await message.answer('Продажа игр происходит по следующему курсу:\n5₽ за 1₺ при покупке до 500₺\n4,8₽ за 1₺ при покупке от 500₺ до 1000₺\n4,5₽ за 1₺ при покупке от 1000₺\n Так как я пока не умею распознавать названия игр, перевожу тебя на живого человека', 
#    reply_markup=types.ReplyKeyboardRemove())
   

@dp.message_handler(lambda message: message.text == "Наши страницы")
async def url_command(message: types.Message):
   await message.answer('Полезные ссылки:', reply_markup=urlkb)

@dp.message_handler(lambda message: message.text == "Extra 1 месяц" or message.text == "Extra 3 месяца" or message.text == "Extra 12 месяцев" or message.text == "DELUXE 1 месяц" or message.text == "DELUXE 3 месяца" or message.text == "DELUXE 12 месяцев" or message.text == "Essential 1 месяц" or message.text == "Essential 3 месяца" or message.text == "Essential 12 месяцев")
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="Подтвердить"),
           types.KeyboardButton(text="К выбору услуг")
       ],
   ]

   keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите ответ"
    )
 
   await message.reply("Подтвердите ваш выбор", reply_markup=keyboard)
   global messageService
   messageService = message.text
   

# @dp.message_handler() #Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
# async def echo(message: types.Message): #Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл пользователь.
#    await message.answer(message.text)

@dp.message_handler()
async def send_welcome(message: types.Message):
    await message.reply("Я вас не понимаю...")



if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)