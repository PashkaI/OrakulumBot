from aiogram import Bot, Dispatcher, executor, types
import datetime
import requests
import sqlite3
from bs4 import BeautifulSoup, Comment
from apscheduler.schedulers.background import BackgroundScheduler

bot = Bot('6024265589:AAEAsVOB-0w-IaeoS3Ach9bZxLxlg9U7MOo')
dp = Dispatcher(bot)
def get_today():
    return datetime.date.today()
def get_yesterday():
    return datetime.date.today() - datetime.timedelta(days=1)
def get_tomorrow():
    return datetime.date.today() + datetime.timedelta(days=1)

scheduler = BackgroundScheduler()
moon_today = ''
moon_yesterday = ''
moon_tomorrow = ''

def MoonDay(data_url):
    global moon_today, moon_yesterday, moon_tomorrow
    url = f"https://www.mingli.ru/{data_url.strftime('%d-%m-%Y')}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    try:  # Вытягиваем значения для Лунного дня
         moon = soup.find('div', class_='Content').find('div', class_='firstInfo').find('div', class_='MoonDay') \
                       .find_all(string=lambda text: isinstance(text, Comment))[1].split('DNone">')[1][:-13]
    except:
        moon = ''
    # записываем данные в нужную переменную
    if data_url == get_today():
        moon_today = moon
    elif data_url == get_yesterday():
        moon_yesterday = moon
    elif data_url == get_tomorrow():
        moon_tomorrow = moon
    return moon

scheduler.add_job(MoonDay, 'cron', hour=6, minute=53, second=20, args=[get_today()])
scheduler.add_job(MoonDay, 'cron', hour=6, minute=53, second=30, args=[get_yesterday()])
scheduler.add_job(MoonDay, 'cron', hour=6, minute=53, second=40, args=[get_tomorrow()])
scheduler.start()

@dp.message_handler(commands=['start'])
async def main(message):
    name = message.from_user.first_name
    nameid = message.from_user.id
    conn = sqlite3.connect('testdata.sql')                      # strana INTEGER
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), '
                'pass varchar(50), strana integer)')
    cur.execute("SELECT * FROM users WHERE name=? AND pass=?", (name, nameid))
    existing_record = cur.fetchone()
    if existing_record:
        await message.answer( "Приветствую тебя снова")
    else:
        cur.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, nameid))
        conn.commit()
        #bot.send_message(message.chat.id, "Запись успешно добавлена.")   .from_user.first_name
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('📍 Украина', callback_data='Ukr')
    btn2 = types.InlineKeyboardButton('📍 Польша', callback_data='Pol')
    btn3 = types.InlineKeyboardButton('️️📍 США', callback_data='Usa')
    markup.row(btn1, btn2, btn3)
    await message.answer(               f'Привет, <b>{name}.</b> '
                                        f'\nДобро пожаловать в сообщество эзотериков :)'
                                        f'\nДля корректировки времени нажми '
                                        f'\nНа  <b>Страну</b> где ты есть'
                                        ,parse_mode='html', reply_markup=markup)

@dp.message_handler(commands=['show_me_the_users'])
async def allusers(message):
    conn = sqlite3.connect('testdata.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users: info += f'Name: {el[1]}, ID:{el[2]}, Strana:{el[3]}\n'
    cur.close()
    conn.close()
    await message.answer(info)
    #await bot.send_message(chat_id=237863350, text=info)
@dp.message_handler(commands=['time'])
async def send_time(message):
    today = get_today()
    test = MoonDay(today)
    print(today)
    print(test)
    current_time = datetime.datetime.now() # получаем текущую дату и время и форматируем ее в строку
    await message.answer(f"Сейчас   : {current_time.strftime('%d-%m-%Y  %H:%M')}"
                         f"\nВчера   : {(current_time - datetime.timedelta(days=1)).strftime('%d-%m-%Y')}"
                         f"\nЗавтра  : {(current_time + datetime.timedelta(days=1)).strftime('%d-%m-%Y')}"
                         f"\n================================"
                         f"\nToday :  {get_today().strftime('%d-%m-%Y  %H:%M:%S')}"
                         f"\n================================"
                         f"\nToday :  {test}"
                         )
@dp.message_handler(commands=['moon'])
async def Moon(message: types.message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Yesterday', callback_data='yesterday')
    btn2 = types.InlineKeyboardButton('Today', callback_data='today')
    btn3 = types.InlineKeyboardButton('Tomorrow', callback_data='tomorrow')
    markup.row(btn1, btn2, btn3)
    await message.answer('Показывать лунный день на сегодня', reply_markup=markup)

@dp.callback_query_handler()
async def callback(call):
    global moon_today, moon_yesterday, moon_tomorrow
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Yesterday', callback_data='yesterday')
    btn2 = types.InlineKeyboardButton('Today', callback_data='today')
    btn3 = types.InlineKeyboardButton('Tomorrow', callback_data='tomorrow')
    markup.row(btn1, btn2, btn3)
    if call.data == 'yesterday':
        if not moon_yesterday:
            moon_yesterday = 'Not Responsing'
        await bot.edit_message_text(text=f'{get_yesterday().strftime("%d-%m-%Y")}'
                                         f'\n-----------'
                                         f'\n{moon_yesterday}'
                                    , chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=markup)
    elif call.data == 'today':
        if not moon_today:
            moon_today = 'Not Responsing'
        await bot.edit_message_text(text=f'{get_today().strftime("%d-%m-%Y")}'
                                         f'\n-----------'
                                         f'\n{moon_today}'
                                    ,chat_id=call.message.chat.id, message_id=call.message.message_id,  reply_markup=markup)
    elif call.data == 'tomorrow':
        if not moon_tomorrow:
            moon_tomorrow = 'Not Responsing'
        await bot.edit_message_text(text=f'{get_tomorrow().strftime("%d-%m-%Y")}'
                                         f'\n-----------'
                                         f'\n{moon_tomorrow}'
                                    , chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=markup)
    elif call.data == 'Ukr':
        nameid = call.from_user.id
        conn = sqlite3.connect('testdata.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
        existing_record = cur.fetchone()
        if existing_record:
            # Обновляем запись в базе данных
            cur.execute("UPDATE users SET strana = ? WHERE pass = ?", (2, nameid))
            conn.commit()
            await bot.send_message(call.message.chat.id, 'Вы выбрали Украина UTC+2')
        cur.close()
        conn.close()

    elif call.data == 'Pol':
        nameid = call.from_user.id
        conn = sqlite3.connect('testdata.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
        existing_record = cur.fetchone()
        if existing_record:
            # Обновляем запись в базе данных
            cur.execute("UPDATE users SET strana = ? WHERE pass = ?", (1, nameid))
            conn.commit()
            await bot.send_message(call.message.chat.id, 'Вы выбрали Польша UTC+1')
        cur.close()
        conn.close()

# if __name__ == '__main__':
#     today = get_today()
#     MoonDay(today)
#     yesterday = get_yesterday()
#     MoonDay(yesterday)
#     tomorrow = get_tomorrow()
#     MoonDay(tomorrow)

executor.start_polling(dp)