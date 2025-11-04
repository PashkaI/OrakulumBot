from aiogram import Bot, Dispatcher, executor, types
import datetime
import time
import requests
import sqlite3
from bs4 import BeautifulSoup, Comment
from apscheduler.schedulers.background import BackgroundScheduler

bot = Bot('6024265589:AAEAsVOB-0w-IaeoS3Ach9bZxLxlg9U7MOo')
dp = Dispatcher(bot)
#  ============= Узнаём время на сегодня, завтра и вчера =============
def get_now():
    return datetime.datetime.now()
def get_today():
    #return datetime.date.today()
    return datetime.datetime.now()
def get_yesterday():
    #return datetime.date.today() - datetime.timedelta(days=1)
    return datetime.datetime.now() - datetime.timedelta(days=1)
def get_tomorrow():
    #return datetime.date.today() + datetime.timedelta(days=1)
    return datetime.datetime.now() + datetime.timedelta(days=1)

scheduler = BackgroundScheduler()
moon_today = ''
moon_yesterday = ''
moon_tomorrow = ''
content_today = ''
content_yesterday = ''
content_tomorrow = ''

#======== Вытягиваем значений ============
def MoonDay(data_url):
    global moon_today, moon_yesterday, moon_tomorrow, content_today, content_yesterday, content_tomorrow
    url = f"https://www.mingli.ru/{data_url.strftime('%d-%m-%Y')}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    try:# Вытягиваем значения для Лунного дня
        moon = soup.find('div', class_='Content').find('div', class_='firstInfo').find('div', class_='MoonDay') \
                       .find_all(string=lambda text: isinstance(text, Comment))[1].split('DNone">')[1][:-13]
    except:
        moon = ''
    time.sleep(3)
    try:# Вытягиваем на три дня со звёздами
        content = soup.find('div', class_='Content')
    except:
        content = ''
    # записываем данные в нужную переменную
    if data_url.strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'):
        moon_today = moon
        content_today = content
        print(f"Выгрузка:  {' '.join(moon_today.split()[0:3])}  {get_now()}  {data_url}")
        print(f"Выгрузка:  {content_today.find('h5', class_='CzjanChu').text}")
    elif data_url.strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'):
        moon_yesterday = moon
        content_yesterday = content
        print(f"Выгрузка:  {' '.join(moon_yesterday.split()[0:3])}  {get_now()}  {data_url}")
        print(f"Выгрузка:  {content_yesterday.find('h5', class_='CzjanChu').text}")
    elif data_url.strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'):
        moon_tomorrow = moon
        content_tomorrow = content
        print(f"Выгрузка:  {' '.join(moon_tomorrow.split()[0:3])}  {get_now()}  {data_url}")
        print(f"Выгрузка:  {content_tomorrow.find('h5', class_='CzjanChu').text}")

    # return moon
def Printersimbols():
    print('=======================================================')



#======== Обработка Шедулеров ============

scheduler.add_job(MoonDay, 'cron', hour=0, minute=0, second=20, args=[get_yesterday()])
scheduler.add_job(MoonDay, 'cron', hour=0, minute=0, second=30, args=[get_today()])
scheduler.add_job(MoonDay, 'cron', hour=0, minute=0, second=40, args=[get_tomorrow()])
scheduler.add_job(Printersimbols, 'cron', hour=0, minute=3, second=45)
scheduler.add_job(MoonDay, 'cron', hour=0, minute=1, second=20, args=[get_yesterday()])
scheduler.add_job(MoonDay, 'cron', hour=0, minute=1, second=30, args=[get_today()])
scheduler.add_job(MoonDay, 'cron', hour=0, minute=1, second=40, args=[get_tomorrow()])
scheduler.add_job(Printersimbols, 'cron', hour=0, minute=8, second=45)

scheduler.add_job(MoonDay, 'cron', hour=12, minute=17, second=20, args=[get_yesterday()])
scheduler.add_job(MoonDay, 'cron', hour=12, minute=17, second=25, args=[get_today()])
scheduler.add_job(MoonDay, 'cron', hour=12, minute=17, second=30, args=[get_tomorrow()])

scheduler.start()

@dp.message_handler(commands=['start'])
async def main(message):
    name = message.from_user.first_name
    nameid = message.from_user.id
    conn = sqlite3.connect('testdata.sql')                      # utc INTEGER
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), '
                'pass varchar(50), utc integer, alarm varchar(8))')
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
@dp.message_handler(commands=['test'])
async def maintest(message):
    now = get_now()
    name = message.from_user.first_name
    usertime = message.date
    nameid = message.from_user.id
    conn = sqlite3.connect('testdata.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
    existing_record = cur.fetchone()
    if existing_record:
        utc = existing_record[-2]
        timedelta = usertime + datetime.timedelta(hours=utc)
    cur.close()
    conn.close()
    await message.answer(               f'Привет, <b>{name}.</b> '
                                        f'\n==Из message user=='
                                        f'\n  <b>{usertime}</b>'
                                        f'\n==Переменная  Now =='
                                        f'\n  <b>{now.strftime("%d-%m-%Y  %H:%M")}</b>'
                                        f'\n=================='
                                        f'\n  <b>{timedelta}</b>'
                                        ,parse_mode='html')

@dp.message_handler(commands=['show_me_the_users'])
async def allusers(message):
    conn = sqlite3.connect('testdata.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users: info += f'Name: {el[1]}, ID:{el[2]}, utc:{el[3]}, alert:{el[4]}\n'
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    await message.answer(f'{count}\n{info}')
    # await bot.send_message(chat_id=237863350, text=info)
    # await bot.send_message(chat_id=678537666, text='Привет Татьяна. Как твои дела?')
@dp.message_handler(commands=['time'])
async def send_time(message):
    usertime = message.date
    nameid = message.from_user.id
    conn = sqlite3.connect('testdata.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
    existing_record = cur.fetchone()
    if existing_record:
        utc = existing_record[-2]
        timedelta = usertime + datetime.timedelta(hours=utc)
    cur.close()
    conn.close()
    if timedelta.strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'): testmoon = moon_today  #test = MoonDay(get_today())
    if timedelta.strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'): testmoon = moon_tomorrow  #test = MoonDay(get_tomorrow())
    if timedelta.strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'): testmoon = moon_yesterday  #test = MoonDay(get_yesterday())
    if timedelta.strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'): testcontent = content_today  #test = MoonDay(get_today())
    if timedelta.strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'): testcontent = content_tomorrow  #test = MoonDay(get_tomorrow())
    if timedelta.strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'): testcontent = content_yesterday  #test = MoonDay(get_yesterday())

    DSymbol = testcontent.find('div', class_='firstInfo').find('h5', class_='CzjanChu').text
    DSymbolo = testcontent.find('div', class_='firstInfo').find('p', class_='CzjanChu').text
    # print(timedelta.strftime('%d-%m-%Y'))
    # print(get_today().strftime('%d-%m-%Y'))
    # print(get_tomorrow().strftime('%d-%m-%Y'))
    # today = get_today()
    # test = MoonDay(today)
    # print(today)
    # print(test)
    current_time = datetime.datetime.now() # получаем текущую дату и время и форматируем ее в строку
    await message.answer(f"Время сервера : {current_time.strftime('%d-%m-%Y  %H:%M')}"
                         f"\n================"
                         f"\nВаше время  : {timedelta.strftime('%d-%m-%Y  %H:%M')}"
                         f"\n================"
                         f"\nToday :  {testmoon}"
                         f"\n================"
                         f"\nToday :  {DSymbol}"
                         f"\nToday :  {DSymbolo}"
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
    global moon_today, moon_yesterday, moon_tomorrow, content_today, content_yesterday, content_tomorrow
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
                                         f'\n-----------'
                                         f"\n{content_yesterday.find('div', class_='firstInfo').find('h5', class_='CzjanChu').text}"
                                         f"\n{content_yesterday.find('div', class_='firstInfo').find('p', class_='CzjanChu').text}"
                                    , chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=markup)
    elif call.data == 'today':
        if moon_today is None or content_today is None:
            moon_today = 'Not Responsing'
            content_today = 'Not Responsing'
        await bot.edit_message_text(text=f'{get_today().strftime("%d-%m-%Y")}'
                                         f'\n-----------'
                                         f'\n{moon_today}'
                                         f'\n-----------'
                                         f"\n{content_today.find('div', class_='firstInfo').find('h5', class_='CzjanChu').text}"
                                         f"\n{content_today.find('div', class_='firstInfo').find('p', class_='CzjanChu').text}"
                                    ,chat_id=call.message.chat.id, message_id=call.message.message_id,  reply_markup=markup)
    elif call.data == 'tomorrow':
        if not moon_tomorrow:
            moon_tomorrow = 'Not Responsing'
        await bot.edit_message_text(text=f'{get_tomorrow().strftime("%d-%m-%Y")}'
                                         f'\n-----------'
                                         f'\n{moon_tomorrow}'
                                         f'\n-----------'
                                         f"\n{content_tomorrow.find('div', class_='firstInfo').find('h5', class_='CzjanChu').text}"
                                         f"\n{content_tomorrow.find('div', class_='firstInfo').find('p', class_='CzjanChu').text}"
                                    , chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=markup)
    elif call.data == 'Ukr':
        nameid = call.from_user.id
        usertime = call.message.date
        conn = sqlite3.connect('testdata.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
        existing_record = cur.fetchone()
        if existing_record:
            # Обновляем запись в базе данных
            cur.execute("UPDATE users SET utc = ? WHERE pass = ?", (1, nameid))
            conn.commit()
            # Получаем обновленную запись из базы данных
            cur.execute("SELECT utc FROM users WHERE pass=?", (nameid,))
            existing_record = cur.fetchone()
        utc = existing_record[-1]
        timedelta = usertime + datetime.timedelta(hours=utc)
        cur.close()
        conn.close()
        await bot.send_message(call.message.chat.id, f'Вы выбрали Украина UTC+2\n{timedelta}')

    elif call.data == 'Pol':
        nameid = call.from_user.id
        usertime = call.message.date
        conn = sqlite3.connect('testdata.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
        existing_record = cur.fetchone()
        if existing_record:
            # Обновляем запись в базе данных
            cur.execute("UPDATE users SET utc = ? WHERE pass = ?", (0, nameid))
            conn.commit()
            # Получаем обновленную запись из базы данных
            cur.execute("SELECT utc FROM users WHERE pass=?", (nameid,))
            existing_record = cur.fetchone()
        utc = existing_record[-1]
        timedelta = usertime + datetime.timedelta(hours=utc)
        cur.close()
        conn.close()
        await bot.send_message(call.message.chat.id, f'Вы выбрали Польша UTC+1\n{timedelta}')

    elif call.data == 'Usa':
        nameid = call.from_user.id
        usertime = call.message.date
        conn = sqlite3.connect('testdata.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
        existing_record = cur.fetchone()
        if existing_record:
            # Обновляем запись в базе данных
            cur.execute("UPDATE users SET utc = ? WHERE pass = ?", (-6, nameid))
            conn.commit()
            # Получаем обновленную запись из базы данных
            cur.execute("SELECT utc FROM users WHERE pass=?", (nameid,))
            existing_record = cur.fetchone()
        utc = existing_record[-1]
        timedelta = usertime + datetime.timedelta(hours=utc)
        cur.close()
        conn.close()
        await bot.send_message(call.message.chat.id, f'Вы выбрали США UTC-4\n{timedelta}')


if __name__ == '__main__':
    today = get_today()
    MoonDay(today)
    yesterday = get_yesterday()
    MoonDay(yesterday)
    tomorrow = get_tomorrow()
    MoonDay(tomorrow)

executor.start_polling(dp)
