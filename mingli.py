import telebot
import webbrowser
import sqlite3
from telebot import types
from datetime import datetime
import datetime
import requests
from bs4 import BeautifulSoup, Comment
from apscheduler.schedulers.background import BackgroundScheduler


bot = telebot.TeleBot('6024265589:AAEAsVOB-0w-IaeoS3Ach9bZxLxlg9U7MOo')

scheduler = BackgroundScheduler()
moon = ''
hours = ''
content = ''

# ================= Описание для часа на день ====================
def DayAnimals(data_url=datetime.datetime.now().strftime("%d-%m-%Y")):
    url = f"https://www.mingli.ru/{data_url}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    DayHour = ''
    Animals = ''
    try:
        if datetime.datetime.now().time() >= datetime.time(23, 1) and datetime.datetime.now().time() <= datetime.time( 23, 59):
            DayHour = soup.find('div', class_='Content').findAll('td')[-1]
            Animals = 'Час Крысы 🐁 с 23:00 до 01:00'
        elif datetime.datetime.now().time() >= datetime.time(21, 1) and datetime.datetime.now().time() <= datetime.time(23, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-2]
            Animals = 'Час Свиньи 🐖 с 21:00 до 23:00'
        elif datetime.datetime.now().time() >= datetime.time(19, 1) and datetime.datetime.now().time() <= datetime.time(21, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-3]
            Animals = 'Час Собаки 🐕 с 19:00 до 21:00'
        elif datetime.datetime.now().time() >= datetime.time(17, 1) and datetime.datetime.now().time() <= datetime.time(19, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-4]
            Animals = 'Час Петуха 🐓 с 17:00 до 19:00'
        elif datetime.datetime.now().time() >= datetime.time(15, 1) and datetime.datetime.now().time() <= datetime.time(17, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-5]
            Animals = 'Час Обезьяны 🐒 с 15:00 до 17:00'
        elif datetime.datetime.now().time() >= datetime.time(13, 1) and datetime.datetime.now().time() <= datetime.time(15, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-6]
            Animals = 'Час Козы 🐐 с 13:00 до 15:00'
        elif datetime.datetime.now().time() >= datetime.time(11, 1) and datetime.datetime.now().time() <= datetime.time(13, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-7]
            Animals = 'Час Лошади 🐎 с 11:00 до 13:00'
        elif datetime.datetime.now().time() >= datetime.time(9, 1) and datetime.datetime.now().time() <= datetime.time(11, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-8]
            Animals = 'Час Змеи 🐍 с 09:00 до 11:00'
        elif datetime.datetime.now().time() >= datetime.time(7, 1) and datetime.datetime.now().time() <= datetime.time( 9, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-9]
            Animals = 'Час Дракона 🐉 с 07:00 до 09:00'
        elif datetime.datetime.now().time() >= datetime.time(5, 1) and datetime.datetime.now().time() <= datetime.time(7, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-10]
            Animals = 'Час Кролика 🐇 с 05:00 до 07:00'
        elif datetime.datetime.now().time() >= datetime.time(3, 1) and datetime.datetime.now().time() <= datetime.time(5, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-11]
            Animals = 'Час Тигра 🐅 с 03:00 до 05:00'
        elif datetime.datetime.now().time() >= datetime.time(1, 1) and datetime.datetime.now().time() <= datetime.time(3, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-12]
            Animals = 'Час Быка 🐂 с 01:00 до 03:00'
        elif datetime.datetime.now().time() >= datetime.time(0, 00) and datetime.datetime.now().time() <= datetime.time(1, 00):
            DayHour = soup.find('div', class_='Content').findAll('td')[-13]
            Animals = 'Час Крысы 🐁 с 23:00 до 01:00'
    except:
        DayHour = ''

    return DayHour, Animals

# ========================== Описание для лунного дня ==============
def MoonDay(data_url=datetime.datetime.now().strftime("%d-%m-%Y")):
    global moon
    url = f"https://www.mingli.ru/{data_url}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    try:  # Вытягиваем значения для Лунного дня
        moon = soup.find('div', class_='Content').find('div', class_='firstInfo').find('div', class_='MoonDay') \
                      .find_all(string=lambda text: isinstance(text, Comment))[1].split('DNone">')[1][:-13]
    except:
        moon = ''
    return moon
scheduler.add_job(MoonDay, 'cron', hour=9, minute=31)

# ============== Описание на текущий день и символы со звёздами ==============
def StarsDay(data_url=datetime.datetime.now().strftime("%d-%m-%Y")):
    global content
    url = f"https://www.mingli.ru/{data_url}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    content = soup.find('div', class_='Content').find('div', class_='firstInfo')
    return content
scheduler.add_job(StarsDay, 'cron', hour=8, minute=47)

# ============== Описание для двухчасовок ==============================
def Hours(data_url=datetime.datetime.now().strftime("%d-%m-%Y")):
    global hours
    url = f"https://www.mingli.ru/{data_url}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    hours = soup.find('div', class_='Content').findAll('td')[-5]
    return hours
scheduler.add_job(Hours, 'cron', hour=7, minute=2)


# ============== Обработка запросов по коммандам Бота =================================================================
@bot.message_handler(commands=['start'])
def main(message):
    name = message.from_user.first_name
    nameid = message.from_user.id
    conn = sqlite3.connect('userdata.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    cur.execute("SELECT * FROM users WHERE name=? AND pass=?", (name, nameid))
    existing_record = cur.fetchone()
    if existing_record:
        bot.send_message(message.chat.id, "Приветствую тебя снова")
    else:
        cur.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, nameid))
        conn.commit()
        #bot.send_message(message.chat.id, "Запись успешно добавлена.")
    cur.close()
    conn.close()
    bot.send_message(message.chat.id,   f'Привет, <b>{message.from_user.first_name}.</b> '
                                        f'\nДобро пожаловать в сообщество эзотериков :)'
                                        f'\nПредлагаю для начала почитать справку :'
                                        f'\nДля этого тапни на <b> /help </b>'
                                        ,parse_mode='html')

@bot.message_handler(commands=['show_me_the_users'])
def allusers(message):
    conn = sqlite3.connect('userdata.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users: info += f'Name: {el[1]}, ID:{el[2]}\n'
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, info)
    #bot.send_message(237863350, 'Привет, Я тебя нашёл!')
    # bot.send_message(5089599713, 'Аххахах. Вот и всё. Теперь ты от меня не отделаешься. Пашка меня наконец-то допилил и'
    #                              'теперь я полностью рабочий AI ')

@bot.message_handler(commands=['profile'])
def profile(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    bot.send_message(message.chat.id,   f'\n👤  <b>Профиль пользователя</b>'
                                        f'\n-------------------------------'
                                        f'\nВы зарегистрированы в системе под именем : {message.from_user.first_name}.'
                                        f' Для точных прогнозов нужна информация для определения точной даты и времени.'
                                        f' В зависимости от вашего местоположения бот скорректирует свои часы'
                                        # f'\n Для этого надо нажать кнопку  📍 <b>Геоданные</b>'
                                        # f'\nТекущая дата и время <b> /location </b>'
                                        f'\nПриятного пользования'
                          ,reply_markup=markup, parse_mode='html')

# ======================================================================================================
#                 Пример работы функции на отправке сообщения пользователю
# ======================================================================================================

def send_moon_to_user(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    bot.send_message(chat_id, f'\n👤  <b>Лунный день :</b>'
                              f'\n-------------------------------'
                              f'\n Значение - : {moon}.'
                      , reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['mooner'])
def mooner(message):
    send_moon_to_user(message.chat.id)
scheduler.add_job(send_moon_to_user, 'cron', hour=9, minute=32, args=[237863350])

# ========================================================================================================


@bot.message_handler(commands=['main'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('📅  Показать прогноз на сегодня', callback_data='today')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('🌓 Лунный День', callback_data='moon')
    btn3 = types.InlineKeyboardButton('️️⭐️  Звёзды', callback_data='stars')
    markup.row(btn2, btn3)
    btn4 = types.InlineKeyboardButton('🧭 Все часы', callback_data='hours')
    btn5 = types.InlineKeyboardButton('❓ Помощь', callback_data='help')
    markup.row(btn4, btn5)

    bot.send_message(message.chat.id, f'\n💡  <b>Меню</b>'
                                      f'\n  ------------'
                                      f'\n  Быстрое использование всех команд бота.'
                                      f'\nПрогноз на день или на час по китайскому календарю.'
                                      f' Показать лунный прогноз на день и узнать символ дня.'
                                      f'\nВывод справичной информации.'

                                    ,reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['time'])
def send_time(message):
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") # получаем текущую дату и время и форматируем ее в строку
    bot.reply_to(message, f"Выгрузка по времени ТЕСТ: {current_time}") # отправляем сообщение с текущей датой и временем

@bot.message_handler(commands=['test1'])
def send_time1():
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    bot.send_message(chat_id=237863350, text=f"Информация выгружена: {current_time}")

scheduler.add_job(send_time1, 'cron', hour=10, minute=00)
scheduler.start()

@bot.message_handler(commands=['test'])
def test(message):

    bot.reply_to(message, f"Текущая дата и время: {hours}")

@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://google.com')

@bot.message_handler(commands=['help'])
def help(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    bot.send_message(message.chat.id,   f'\n🔹  <b>Основные команды</b>'
                                        f'\n'
                                        f'\nГлавное меню <b> /main </b>'
                                        f'\nПрогноз на день <b> /day </b>'
                                        f'\nПрогноз на Час <b> /hour </b>'
                                        f'\nЛунный прогноз на день <b> /moon </b>'
                                        f'\nCимволы дня по звёздам<b> /stars </b>'
                                        f'\nПрофиль пользователя <b> /profile </b>'
                                        f'\nТекущая дата и время <b> /time </b>'
                                        f'\n'
                                        f'\n🔹  <b>Что умеет этот бот:</b>'
                                        f'\n'
                                        f'\nРобот выводит прогноз на день или на час по китайскому календарю.'
                                        f' А так же можно посмотреть лунный прогноз на день и символ дня.'
                                        f' В будущем возможно ещё сделаю вывод информации по Тибетским праздникам.'
                                        f'\n  --------------------------------'
                                        f'\n📅 Для того чтобы посмотреть прогноз на нужную вам дату, её необходимо'
                                        f' ввести в чате бота в формате DD-MM-YYYY (Например: 17-03-2023).'
                                        f'\n'
                                        f'\nПо работе бота писать: @Rts_support'
                          ,reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['moon'])
def moonday(message):
    waitfor = bot.send_message(message.chat.id, 'Ожидайте загрузки ... ⌛️')
    #params = MoonDay()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    bot.edit_message_text(              f'\n  🌓 <b> Лунный прогноз на день </b>'
                                        f'\n  --------------------------------'
                                        f'\n   {moon}'
                          ,chat_id=waitfor.chat.id, message_id=waitfor.message_id, reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['day'])
def today(message):
    waitfor = bot.send_message(message.chat.id, 'Ожидайте загрузки ... ⌛️')
    #params = StarsDay()
    try:
        DSymbol = content.find('h5', class_='CzjanChu').text
    except:
        DSymbol = ''
    try:
        DSymbolo = content.find('p', class_='CzjanChu').text
    except:
        DSymbolo = ''
    try:
        DayPlus = content.find('p', class_='PlusMinus').text
    except:
        DayPlus = ''
    try:
        DayMinus = content.findAll('p', class_='PlusMinus')[1].text
    except:
        DayMinus = ''
    try:
        DMoon = content.find('div', class_='MoonDay').text
    except:
        DMoon = ''

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('↩️  Назад', callback_data='back')
    btn2 = types.InlineKeyboardButton('🔎  Час на сейчас', callback_data='hour')
    markup.row(btn1, btn2)
    bot.edit_message_text(              f'\n 📅  <b>Сегодня :   {datetime.datetime.now().strftime("%d")}-'
                                        f'{datetime.datetime.now().strftime("%m")}-'
                                        f'{datetime.datetime.now().strftime("%Y")}</b>'
                                        f'\n-------------------------------'
                                        f'\n  - <b><u> {DSymbol}</u></b>'
                                        f'\n   -  {DSymbolo}'
                                        f'\n -------------------------------------'
                                        f'\n  ✅ -  {DayPlus}'
                                        f'\n  ⛔️ -  {DayMinus}'
                                        f'\n -------------------------------------'
                                        f'\n{str(DMoon).strip()}'
                                    ,chat_id=waitfor.chat.id, message_id=waitfor.message_id, reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['stars'])
def stars(message):
    waitfor = bot.send_message(message.chat.id, 'Ожидайте загрузки ... ⌛️')
    params = StarsDay()
    try:  # Разрушитель года или месяца (Надо подставить слово "Разрушитель")
        collision1 = params.find('h5', class_='red Collision').text  # .split()[-1]
    except:
        collision1 = ''
    try:  # Описание для Разрушителя.
        collision1o = params.findAll('p')[4].text
    except:
        collision1o = ''
    try:  # Второй Разрушитель, если есть первый года или месяца (Надо подставить слово "Разрушитель")
        collision2 = params.findAll('h5', class_='red Collision')[1].text  # .split()[-1]
    except:
        collision2 = ''
    try:  # Описание для Разрушителя.
        collision2o = params.findAll('p')[5].text
    except:
        collision2o = ''
    try:  # Красное ША года
        sha1 = params.find('h5', class_='red Sha').text
    except:
        sha1 = ''
    try:  # Описание для ША
        sha1o = params.find('p', class_='Sha').text
    except:
        sha1o = ''
    try:  # Красное второе ША года
        sha2 = params.findAll('h5', class_='red Sha')[1].text
    except:
        sha2 = ''
    try:  # Описание для ША
        sha2o = params.findAll('p', class_='Sha')[1].text
    except:
        sha2o = ''
    try:  # Позитивный символ для Звезды
        positive1 = params.find('h5', class_='positive SymbolStars').text  # оставить
    except:
        positive1 = ''
    try:  # Описание позитивного символа
        positive1o = params.find('p', class_='SymbolStars').text
    except:
        positive1o = ''
    try:  # Позитивный второй символ для Звезды
        positive2 = params.findAll('h5', class_='positive SymbolStars')[1].text
    except:
        positive2 = ''
    try:  # Описание второго позитивного символа
        positive2o = params.findAll('p', class_='SymbolStars')[2].text
    except:
        positive2o = ''
    try:  # Символ MKD
        symbolMKD = params.find('div', class_='SymbolStars MKD').text
    except:
        symbolMKD = ''
    try:  # Негативный символ для Звезды
        negative = params.find('h5', class_='negative SymbolStars').text
    except:
        negative = ''
    try:  # Описание негативного символа
        negativeo = params.findAll('p', class_='SymbolStars')[1].text
    except:
        negativeo = ''

    stars = collision1.strip()+collision1o+collision2.strip()+collision2o+sha1+sha1o.strip()+sha2+sha2o.strip()\
            +positive1+positive1o+positive2+positive2o+symbolMKD+negative+negativeo

    if collision1: collision1 = '\n ⛔️ - ' + collision1.strip()
    if collision1o: collision1o = '\n' + collision1o
    if collision2: collision2 = '\n ⛔️ - ' + collision2.strip()
    if collision2o: collision2o = '\n' + collision2o
    if sha1: sha1 = '\n ⛔️ - ' + sha1.strip()
    if sha1o: sha1o = '\n' + sha1o.strip()
    if sha2: sha2 = '\n ⛔️ - ' + sha2
    if sha2o: sha2o = '\n' + sha2o.strip()
    if positive1: positive1 = '\n ✅ - ' + positive1
    if positive1o: positive1o = '\n' + positive1o
    if positive2: positive2 = '\n ✅ - ' + positive2
    if positive2o: positive2o = '\n' + positive2o
    if symbolMKD: symbolMKD = '\n 🀄️ - ' + symbolMKD
    if negative: negative = '\n ⛔️ - ' + negative
    if negativeo: negativeo = '\n' + negativeo

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))

    if not stars:
        bot.edit_message_text(
                         f'\n ⭐️<b><u> Cимволы дня и летящие звёзды </u></b>'
                         f'\n---------------------------------------'
                         f'\n Сегодня нет информации'
                         ,chat_id=waitfor.chat.id, message_id=waitfor.message_id, reply_markup=markup, parse_mode='html')
    else:
        bot.edit_message_text(
                         f'\n ⭐️<b> Cимволы дня и летящие звёзды </b>'
                         f'\n---------------------------------------'
                         f' {f"<b>{collision1}</b>" if collision1 else ""}'
                         f' {f"{collision1o}" if collision1 else ""}'
                         f' {f"<b>{collision2}</b>" if collision2 else ""}'
                         f' {f"{collision2o}" if collision2o and collision2 and collision2o != sha1o else ""}'
                         f' {f"<b>{sha1}</b>" if sha1 else ""}'
                         f' {f"{sha1o}" if sha1o and not sha2 else ""}'
                         f' {f"<b>{sha2}</b>" if sha2 else ""}'
                         f' {f"{sha2o}" if not sha1o and sha2o else ""}'
                         f' {f"{sha2o}" if sha2o and sha2 and sha2o == sha1o else ""}'
                         f' {f"<b>{positive1}</b>" if positive1 else ""}'
                         f' {f"{positive1o}" if positive1o and positive1 and positive1o[:-1] != negativeo else ""}'
                         f' {f"<b>{positive2}</b>" if positive2 else ""}'
                         f' {f"{positive2o}" if positive2o else ""}'
                         f' {f"<b>{symbolMKD}</b>" if symbolMKD else ""}'
                         f' {f"<b>{negative}</b>" if negative else ""}'
                         f' {f"{negativeo}" if negativeo else ""}'
                         f' {f"{collision1o}" if not negativeo and negative else ""}'
                         ,chat_id=waitfor.chat.id, message_id=waitfor.message_id, reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['hour'])
def daytimes(message):
    waitfor = bot.send_message(message.chat.id, 'Ожидайте загрузки ... ⌛️')
    params, animails = DayAnimals()
    try: # Пробую получить информацию
        plus_minus = params.findAll('p', class_='PlusMinus')
    except:
        plus_minus = ''
    try:  # Пробую получить информацию
        plus_minuso = params.find('p', class_='PlusMinus').text
    except:
        plus_minuso = ''

    try:  # Описание позитивного часа
        Positive = plus_minus[0].find('span', class_='IconPositive')
    except:
        Positive = ''
    try:  # Описание негативного часа
        Negative = plus_minus[0].find('span', class_='IconNegative')
    except:
        Negative = ''
    try:  # Описание для негативного, если есть позитивный час
        Negative2 = plus_minus[1].find('span', class_='IconNegative')
    except:
        Negative2 = ''
    try:
        Collision = params.find('p', class_='Collision').text
    except:
        Collision = ''
    try:
        SymbolStars = params.findAll('p', class_='SymbolStars')[0].text
    except:
        SymbolStars = ''
    try:
        SymbolStars1 = params.findAll('p', class_='SymbolStars')[1].text
    except:
        SymbolStars1 = ''
    try:
        SymbolStars2 = params.findAll('p', class_='SymbolStars')[2].text
    except:
        SymbolStars2 = ''
    try:
        SymbolStars3 = params.findAll('p', class_='SymbolStars')[3].text
    except:
        SymbolStars3 = ''

    if Positive: Positive = '\n ✅  ' + plus_minuso.strip()
    if Negative: Negative = '\n ⛔️  ' + plus_minuso.strip()
    if Negative2: Negative2 = '\n ⛔️  ' + plus_minus[1].text.strip()
    if Collision: Collision = '\n ➖  ' + Collision.strip()
    if SymbolStars: SymbolStars = '\n -- ' + SymbolStars
    if SymbolStars1: SymbolStars1 = '\n -- ' + SymbolStars1
    if SymbolStars2: SymbolStars2 = '\n -- ' + SymbolStars2
    if SymbolStars3: SymbolStars3 = '\n SymbolStars3 - ' + SymbolStars3

    Negative1 = str(Negative).strip()
    Positive1 = str(Positive).strip()

    ours = Negative1+Positive1

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))

    if not ours:
        bot.edit_message_text(
                         f'\n 🕒<b>  Сейчас {datetime.datetime.now().strftime("%H:%M")} -- {animails}</b>'
                         f'\n'
                         f'\n Нет информации на текущее время.'
                         f'\n Попробуйте посмотреть через час.'
                         ,chat_id=waitfor.chat.id, message_id=waitfor.message_id, reply_markup=markup, parse_mode='html')
    else:
        bot.edit_message_text(
                         f'\n 🕒<b>  Сейчас {datetime.datetime.now().strftime("%H:%M")} '
                         f'\n{animails}</b>'
                         f'\n--------------------------------------'
                         f' {f"{Positive}" if Positive else ""}'
                         f' {f"{Negative}" if Negative else ""}'
                         f' {f"{Negative2}" if Negative2 else ""}'
                         f' {f"{Collision}" if Collision else ""}'
                         f' {f"{SymbolStars}" if SymbolStars else ""}'
                         f' {f"{SymbolStars1}" if SymbolStars1 else ""}'
                         f' {f"{SymbolStars2}" if SymbolStars2 else ""}'
                         f' {f"{SymbolStars3}" if SymbolStars3 else ""}'
                         ,chat_id=waitfor.chat.id, message_id=waitfor.message_id, reply_markup=markup, parse_mode='html')

@bot.callback_query_handler(func=lambda callback: True) # Обработка Запросов Callback =====================================================
def callback_message(callback):
    if callback.data == 'today':
        today(callback.message)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'hours':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Час Крысы 🐁 с 23:00 до 01:00', callback_data='rat'))
        markup.add(types.InlineKeyboardButton('Час Быка 🐂 с 01:00 до 03:00', callback_data='bull'))
        markup.add(types.InlineKeyboardButton('Час Тигра 🐅 с 03:00 до 05:00', callback_data='tiger'))
        markup.add(types.InlineKeyboardButton('Час Кролика 🐇 с 05:00 до 07:00', callback_data='rabbit'))
        markup.add(types.InlineKeyboardButton('Час Дракона 🐉 с 07:00 до 09:00', callback_data='dragon'))
        markup.add(types.InlineKeyboardButton('Час Змеи 🐍 с 09:00 до 11:00', callback_data='snake'))
        markup.add(types.InlineKeyboardButton('Час Лошади 🐎 с 11:00 до 13:00', callback_data='horse'))
        markup.add(types.InlineKeyboardButton('Час Козы 🐐 с 13:00 до 15:00', callback_data='goat'))
        markup.add(types.InlineKeyboardButton('Час Обезьяны 🐒 с 15:00 до 17:00', callback_data='monkey'))
        markup.add(types.InlineKeyboardButton('Час Петуха 🐓 с 17:00 до 19:00', callback_data='rooster'))
        markup.add(types.InlineKeyboardButton('Час Собаки 🐕 с 19:00 до 21:00', callback_data='dog'))
        markup.add(types.InlineKeyboardButton('Час Свиньи 🐖 с 21:00 до 23:00', callback_data='pig'))
        markup.add(types.InlineKeyboardButton('Час Крысы 🐁 с 23:00 до 01:00', callback_data='rat'))
        bot.edit_message_text(        f'\n🧭  <b>Все часы на сегодня</b>'
                                      f'\n  -------------------'
                                      f'\n  Выберите нужную вам двучасовку для того чтобы узнать прогноз.'
                         ,callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)



    elif callback.data == 'back':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('📅  Показать прогноз на сегодня', callback_data='today')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('🌓 Лунный День', callback_data='moon')
        btn3 = types.InlineKeyboardButton('️️⭐️  Звёзды', callback_data='stars')
        markup.row(btn2, btn3)
        btn4 = types.InlineKeyboardButton('🧭 Все часы', callback_data='hours')
        btn5 = types.InlineKeyboardButton('❓ Помощь', callback_data='help')
        markup.row(btn4, btn5)
        bot.edit_message_text(        f'\n💡  <b>Меню</b>'
                                      f'\n  ------------'
                                      f'\n  Быстрое использование всех команд бота.'
                                      f'\nПрогноз на день или на час по китайскому календарю.'
                                      f' Показать лунный прогноз на день и узнать символ дня.'
                                      f'\nВывод справичной информации.'
                         ,callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)


    elif callback.data == 'help':
        help(callback.message)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'moon':
        moonday(callback.message)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'hour':
        daytimes(callback.message)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'stars':
        stars(callback.message)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

#======================================Конец блока для CallBack ========================================================

@bot.message_handler(content_types=['text'])
def fordate(message):
    waitfor = bot.send_message(message.chat.id, 'Ожидайте загрузки ... ⌛️')
    date_str = message.text.strip().lower()
    try:
        date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y')
    except ValueError:
        bot.edit_message_text(f'Дата указана не верно', chat_id=waitfor.chat.id, message_id=waitfor.message_id)
        return
    params = StarsDay(date_str)
    try:
        DSymbol = params.find('h5', class_='CzjanChu').text
    except:
        DSymbol = ''
    try:
        DSymbolo = params.find('p', class_='CzjanChu').text
    except:
        DSymbolo = ''
    try:
        DayPlus = params.find('p', class_='PlusMinus').text
    except:
        DayPlus = ''
    try:
        DayMinus = params.findAll('p', class_='PlusMinus')[1].text
    except:
        DayMinus = ''
    try:
        DMoon = params.find('div', class_='MoonDay').text
    except:
        DMoon = ''
    #================================== Звёзды ===========================================
    try:  # Разрушитель года или месяца (Надо подставить слово "Разрушитель")
        collision1 = params.find('h5', class_='red Collision').text  # .split()[-1]
    except:
        collision1 = ''
    try:  # Описание для Разрушителя.
        collision1o = params.findAll('p')[4].text
    except:
        collision1o = ''
    try:  # Второй Разрушитель, если есть первый года или месяца (Надо подставить слово "Разрушитель")
        collision2 = params.findAll('h5', class_='red Collision')[1].text  # .split()[-1]
    except:
        collision2 = ''
    try:  # Описание для Разрушителя.
        collision2o = params.findAll('p')[5].text
    except:
        collision2o = ''
    try:  # Красное ША года
        sha1 = params.find('h5', class_='red Sha').text
    except:
        sha1 = ''
    try:  # Описание для ША
        sha1o = params.find('p', class_='Sha').text
    except:
        sha1o = ''
    try:  # Красное второе ША года
        sha2 = params.findAll('h5', class_='red Sha')[1].text
    except:
        sha2 = ''
    try:  # Описание для ША
        sha2o = params.findAll('p', class_='Sha')[1].text
    except:
        sha2o = ''
    try:  # Позитивный символ для Звезды
        positive1 = params.find('h5', class_='positive SymbolStars').text  # оставить
    except:
        positive1 = ''
    try:  # Описание позитивного символа
        positive1o = params.find('p', class_='SymbolStars').text
    except:
        positive1o = ''
    try:  # Позитивный второй символ для Звезды
        positive2 = params.findAll('h5', class_='positive SymbolStars')[1].text
    except:
        positive2 = ''
    try:  # Описание второго позитивного символа
        positive2o = params.findAll('p', class_='SymbolStars')[2].text
    except:
        positive2o = ''
    try:  # Символ MKD
        symbolMKD = params.find('div', class_='SymbolStars MKD').text
    except:
        symbolMKD = ''
    try:  # Негативный символ для Звезды
        negative = params.find('h5', class_='negative SymbolStars').text
    except:
        negative = ''
    try:  # Описание негативного символа
        negativeo = params.findAll('p', class_='SymbolStars')[1].text
    except:
        negativeo = ''

    if collision1: collision1 = '\n ⛔️ - ' + collision1.strip()
    if collision1o: collision1o = '\n' + collision1o
    if collision2: collision2 = '\n ⛔️ - ' + collision2.strip()
    if collision2o: collision2o = '\n' + collision2o
    if sha1: sha1 = '\n ⛔️ - ' + sha1.strip()
    if sha1o: sha1o = '\n' + sha1o.strip()
    if sha2: sha2 = '\n ⛔️ - ' + sha2
    if sha2o: sha2o = '\n' + sha2o.strip()
    if positive1: positive1 = '\n ✅ - ' + positive1
    if positive1o: positive1o = '\n' + positive1o
    if positive2: positive2 = '\n ✅ - ' + positive2
    if positive2o: positive2o = '\n' + positive2o
    if symbolMKD: symbolMKD = '\n 🀄️ - ' + symbolMKD
    if negative: negative = '\n ⛔️ - ' + negative
    if negativeo: negativeo = '\n' + negativeo

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    bot.edit_message_text(              f'\n 🗓  <b>Запрос на дату :   {date_str}</b>'
                                        f'\n-------------------------------'
                                        f'\n  - <b><u> {DSymbol}</u></b>'
                                        f'\n   -  {DSymbolo}'
                                        f'\n -------------------------------------'
                                        f'\n  ✅ -  {DayPlus}'
                                        f'\n  ⛔️ -  {DayMinus}'
                                        f'\n -------------------------------------'
                                        f'\n{str(DMoon).strip()}'
                                        f'\n -------------------------------------'
                                        f'\n ⭐️<b> Cимволы дня и летящие звёзды </b>'
                                        f'\n---------------------------------------'
                                        f' {f"<b>{collision1}</b>" if collision1 else ""}'
                                        f' {f"{collision1o}" if collision1 else ""}'
                                        f' {f"<b>{collision2}</b>" if collision2 else ""}'
                                        f' {f"{collision2o}" if collision2o and collision2 and collision2o != sha1o else ""}'
                                        f' {f"<b>{sha1}</b>" if sha1 else ""}'
                                        f' {f"{sha1o}" if sha1o and not sha2 else ""}'
                                        f' {f"<b>{sha2}</b>" if sha2 else ""}'
                                        f' {f"{sha2o}" if not sha1o and sha2o else ""}'
                                        f' {f"{sha2o}" if sha2o and sha2 and sha2o == sha1o else ""}'
                                        f' {f"<b>{positive1}</b>" if positive1 else ""}'
                                        f' {f"{positive1o}" if positive1o and positive1 and positive1o[:-1] != negativeo else ""}'
                                        f' {f"<b>{positive2}</b>" if positive2 else ""}'
                                        f' {f"{positive2o}" if positive2o else ""}'
                                        f' {f"<b>{symbolMKD}</b>" if symbolMKD else ""}'
                                        f' {f"<b>{negative}</b>" if negative else ""}'
                                        f' {f"{negativeo}" if negativeo else ""}'
                                        f' {f"{collision1o}" if not negativeo and negative else ""}'
                                    ,chat_id=waitfor.chat.id, message_id=waitfor.message_id, reply_markup=markup, parse_mode='html')

bot.polling(none_stop=True)