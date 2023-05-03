from aiogram import Bot, Dispatcher, executor, types
import datetime
import requests
import sqlite3
from bs4 import BeautifulSoup, Comment
from apscheduler.schedulers.background import BackgroundScheduler
import os
import logging


bot = Bot('6024265589:AAEAsVOB-0w-IaeoS3Ach9bZxLxlg9U7MOo')
dp = Dispatcher(bot)

# Создаем логгер и задаем уровень логирования
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи в файл
file_handler = logging.FileHandler('log.txt', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Создаем форматер для сообщений
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик в логгер
logger.addHandler(file_handler)

#  ============= Узнаём время на сегодня, завтра и вчера =============
def get_today():
    return datetime.datetime.now()
def get_yesterday():
    return datetime.datetime.now() - datetime.timedelta(days=1)
def get_tomorrow():
    return datetime.datetime.now() + datetime.timedelta(days=1)

scheduler = BackgroundScheduler()
content_today = ''
content_yesterday = ''
content_tomorrow = ''
tibet_today = ''
tibet_yesterday = ''
tibet_tomorrow = ''

#======== Выгрузка прогноза по запросу ============
def StarsDay(data_url):
    print(f'Uploading Chinese content on the date - {data_url}')
    url = f"https://www.mingli.ru/{data_url}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    content = soup.find('div', class_='Content')
    return content
def TibetHolly(data_url):
    print(f'Uploading Tibetian content on the date - {data_url}')
    url = f"https://tibetastromed.ru/docom.php?tdat={data_url}&tipv=0&type=old&lang=ru"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    content = soup.findAll('p')[1].text
    return content

#======== Вытягиваем значений ============
def MoonDay(data_url):
    global content_today, content_yesterday, content_tomorrow, tibet_today, tibet_yesterday, tibet_tomorrow
    if data_url == 1: data_url = get_yesterday()
    if data_url == 2: data_url = get_today()
    if data_url == 3: data_url = get_tomorrow()
    url = f"https://www.mingli.ru/{data_url.strftime('%d-%m-%Y')}"
    urlt = f"https://tibetastromed.ru/docom.php?tdat={data_url.strftime('%m/%d/%Y')}&tipv=0&type=old&lang=ru"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    soupt = BeautifulSoup(requests.get(urlt).text, 'html.parser')
    try:# Вытягиваем контент с сайта
        content = soup.find('div', class_='Content')
        tibet = soupt.findAll('p')[1].text
    except:
        content = ''
        tibet = ''
    # записываем данные в нужную переменную
    if data_url.strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'):
        content_yesterday = content
        tibet_yesterday = tibet
        # print(f"Выгрузка >mingli< {data_url.strftime('%d-%m-%Y')}:  "
        #       f"{content_yesterday.find('h5', class_='CzjanChu').text}   "
        #       f"{get_today().strftime('%d-%m-%Y %H:%M:%S')}")
        # print(f"Выгрузка >tibetastromed< {data_url.strftime('%d-%m-%Y')}:  "
        #       f"{' '.join(tibet_yesterday.split()[:3])}   "
        #       f"{get_today().strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug(f"Loading content for yesterday - {data_url.strftime('%d-%m-%Y')}")
    elif data_url.strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'):
        content_today = content
        tibet_today = tibet
        # print(f"Выгрузка >mingli< {data_url.strftime('%d-%m-%Y')}:  "
        #       f"{content_today.find('h5', class_='CzjanChu').text}   "
        #       f"{get_today().strftime('%d-%m-%Y %H:%M:%S')}")
        # print(f"Выгрузка >tibetastromed< {data_url.strftime('%d-%m-%Y')}:  "
        #       f"{' '.join(tibet_today.split()[:3])}   "
        #       f"{get_today().strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug(f"Loading content for today - {data_url.strftime('%d-%m-%Y')}")
    elif data_url.strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'):
        content_tomorrow = content
        tibet_tomorrow = tibet
        # print(f"Выгрузка >mingli< {data_url.strftime('%d-%m-%Y')}:  "
        #       f"{content_tomorrow.find('h5', class_='CzjanChu').text}   "
        #       f"{get_today().strftime('%d-%m-%Y %H:%M:%S')}")
        # print(f"Выгрузка >tibetastromed< {data_url.strftime('%d-%m-%Y')}:  "
        #       f"{' '.join(tibet_tomorrow.split()[:3])}   "
        #       f"{get_today().strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug(f"Loading content for tomorrow - {data_url.strftime('%d-%m-%Y')}")

    # print(data_url.strftime('%d-%m-%Y'))
    # print(f" get_today - {get_today().strftime('%d-%m-%Y')}")
    # print(f" get_yesterday - {get_yesterday().strftime('%d-%m-%Y')}")
    # print(f" get_tomorrow - {get_tomorrow().strftime('%d-%m-%Y')}")
    logger.debug('=========================================================================')
    logger.debug(f"variable  data_url - {data_url.strftime('%d-%m-%Y')}")
    logger.debug(f"variable  get_today - {get_today().strftime('%d-%m-%Y')}")
    logger.debug(f"variable  get_yesterday - {get_yesterday().strftime('%d-%m-%Y')}")
    logger.debug(f"variable  get_tomorrow - {get_tomorrow().strftime('%d-%m-%Y')}")
    logger.debug('=========================================================================')
    # return moon
def Printersimbols():
    print('=======================================================')

#======== Обработка Шедулеров ============

scheduler.add_job(MoonDay, 'cron', hour=0, minute=0, second=20, args=[1])
scheduler.add_job(MoonDay, 'cron', hour=0, minute=0, second=30, args=[2])
scheduler.add_job(MoonDay, 'cron', hour=0, minute=0, second=40, args=[3])
scheduler.add_job(Printersimbols, 'cron', hour=0, minute=0, second=45)

scheduler.add_job(MoonDay, 'cron', hour=9, minute=19, second=20, args=[1])
scheduler.add_job(MoonDay, 'cron', hour=9, minute=19, second=30, args=[2])
scheduler.add_job(MoonDay, 'cron', hour=9, minute=19, second=40, args=[3])
scheduler.add_job(Printersimbols, 'cron', hour=9, minute=19, second=45)

scheduler.start()

# =================== Определяем время пользователя ======================
def timedelta(nameid):
    db_path = os.path.join("db", "userdata.sql")
    usertime = datetime.datetime.now()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
    existing_record = cur.fetchone()
    if existing_record:
        utc = existing_record[-2]
        timedelta = usertime + datetime.timedelta(hours=utc)
    cur.close()
    conn.close()
    return timedelta

# ============== Обработка запросов по командам Бота ========================
@dp.message_handler(commands=['start'])
async def main(message):
    db_path = os.path.join("db", "userdata.sql")
    name = message.from_user.first_name
    nameid = message.from_user.id
    conn = sqlite3.connect(db_path)                      # utc INTEGER
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), '
                'pass varchar(50), utc integer, alarm varchar(8))')
    cur.execute("SELECT * FROM users WHERE name=? AND pass=?", (name, nameid))
    existing_record = cur.fetchone()
    if existing_record:
        await message.answer( "Приветствую тебя снова")
    else:
        cur.execute("INSERT INTO users (name, pass, utc) VALUES (?, ?, ?)", (name, nameid, 1))
        conn.commit()
        #bot.send_message(message.chat.id, "Запись успешно добавлена.")   .from_user.first_name
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🇺🇦 Украина', callback_data='Ukr')
    btn2 = types.InlineKeyboardButton('🇵🇱 Польша', callback_data='Pol')
    btn3 = types.InlineKeyboardButton('️️🇺🇸 США', callback_data='Usa')
    markup.row(btn1, btn2, btn3)
    await message.answer(               f'  Приветствую, <b>{name}!</b> '
                                        f'\nДобро пожаловать в сообщество эзотериков :)'
                                        f'\nНадеюсь, что описание программы вы уже прочитали.'
                                        f' Если нет,- то воспользуйтесь командой <b> /help </b>'
                                        f'\nДля более точных прогнозов необходимо скорректировать'
                                        f' время в программе. Для этого выберите '
                                        f'нужную  📍 <b>Локацию</b> :'
                                        ,parse_mode='html', reply_markup=markup)

@dp.message_handler(commands=['show_me_the_users'])
async def allusers(message):
    db_path = os.path.join("db", "userdata.sql")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users: info += f'Name: {el[1]}, ID:{el[2]}, utc:{el[3]}\n'
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    await message.answer(f'{count}\n{info}')
    # await bot.send_message(chat_id=237863350, text=info)
    # await bot.send_message(chat_id=237863350, text='Привет Pashka. Как твои дела?')

@dp.message_handler(commands=['main'])
async def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('⛩  Тибетский прогноз на сегодня', callback_data='tibet')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('📅  Китайский прогноз на сегодня', callback_data='today')
    markup.row(btn2)
    btn3 = types.InlineKeyboardButton('🌓 Лунный день', callback_data='moon')
    btn4 = types.InlineKeyboardButton('️️⭐️  Звёзды', callback_data='stars')
    markup.row(btn3, btn4)
    btn5 = types.InlineKeyboardButton('🧭 Все часы', callback_data='hours')
    btn6 = types.InlineKeyboardButton('❓ Помощь', callback_data='help')
    markup.row(btn5, btn6)
    await message.answer(             f'\n💡  <b>Меню</b>'
                                      f'\n  ------------'
                                      f'\n  Быстрое использование всех команд бота.'
                                      f'\n- Прогноз на день или на час по китайскому календарю.'
                                      f'\n- Тибетский прогноз (праздники, стрижка, поездки)'
                                      f'\n- Лунный прогноз на день'
                                      f'\n- Что говорят звёзды на сегодня'
                                      f'\n- Вывод справочной информации.'
                                    ,reply_markup=markup, parse_mode='html')

@dp.message_handler(commands=['time'])
async def maintest(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id

    diff_hours = (get_today() - timedelta(nameid)).total_seconds() / 3600
    diff_hours = round(diff_hours)
    if diff_hours == 0: diff_hours = 'Польша 🇵🇱'
    if diff_hours == -1: diff_hours = 'Украина  🇺🇦'
    if diff_hours == 6: diff_hours = 'США 🇺🇸'
    await message.answer(
        f'<b><u>Проверка локации :</u></b>'
        f'\nВ настройках была выбрана страна {diff_hours}'
        f'\nВаша текущая дата и время :'
        f'\n  <b>{timedelta(nameid).strftime("%d-%m-%Y  %H:%M")}</b>'
        f'\nВ любое время вы можете изменить свою локацию в настройках профиля /profile'
        # f'\n{diff_hours}'
        ,parse_mode='html')


@dp.message_handler(commands=['help'])
async def help(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    await message.answer(               f'\n🔹  <b>Основные команды</b>'
                                        f'\n'
                                        f'\n-Главное меню <b> /main </b>'
                                        f'\n-Китайский прогноз на день <b> /day </b>'
                                        f'\n-Китайский прогноз на Час <b> /hour </b>'
                                        f'\n-Тибетский прогноз на день <b> /tibet </b>'
                                        f'\n-Лунный прогноз на день <b> /moon </b>'
                                        f'\n-Cимволы дня по звёздам<b> /stars </b>'
                                        f'\n-Профиль пользователя <b> /profile </b>'
                                        f'\n-Проверка времени и текущей локации <b> /time </b>'
                                        f'\n'
                                        f'\n🔹  <b>Что умеет этот бот:</b>'
                                        f'\n'
                                        f'\nРобот выводит прогноз на день или на час по китайскому календарю.'
                                        f' Прогноз по тибетским праздникам, рекомендуемое время стрижки и поездок.'
                                        f' А так же можно посмотреть лунный прогноз на день и символ дня.'
                                        f'\n  --------------------------------'
                                        f'\n📅 Для того чтобы посмотреть прогноз на нужную вам дату, её необходимо'
                                        f' ввести в чате бота в формате DD-MM-YYYY (Например: 17-03-2023).'
                                        f'\n  --------------------------------'
                                        f'\n⏱ Сделать корректировку времени можно в профиле пользователя'
                                        f'\n'
                                        f'\nПо работе бота писать: @Rts_support'
                          ,reply_markup=markup, parse_mode='html')

@dp.message_handler(commands=['profile'])
async def profile(message):
    db_path = os.path.join("db", "userdata.sql")
    name = message.from_user.first_name
    nameid = message.from_user.id
    conn = sqlite3.connect(db_path)                      # utc INTEGER
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), '
                'pass varchar(50), utc integer, alarm varchar(8))')
    cur.execute("SELECT * FROM users WHERE name=? AND pass=?", (name, nameid))
    existing_record = cur.fetchone()
    if not existing_record:
        cur.execute("INSERT INTO users (name, pass, utc) VALUES (?, ?, ?)", (name, nameid, 1))
        conn.commit()
        #bot.send_message(message.chat.id, "Запись успешно добавлена.")   .from_user.first_name
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🇺🇦 Украина', callback_data='Ukr')
    btn2 = types.InlineKeyboardButton('🇵🇱 Польша', callback_data='Pol')
    btn3 = types.InlineKeyboardButton('️️🇺🇸 США', callback_data='Usa')
    markup.row(btn1, btn2, btn3)
    btn4 = types.InlineKeyboardButton('↩️  Назад', callback_data='back')
    markup.row(btn4)
    await message.answer(               f'\n👤  <b>Профиль пользователя</b>'
                                        f'\n-------------------------------'
                                        f'\nВы зарегистрированы в системе под именем : {name}.'
                                        f' Для точных прогнозов нужна информация относительно даты и времени,'
                                        f' в зависимости от вашего местоположения бот скорректирует свои часы'
                                        f'\n Выберите вашу 📍 <b>Локацию</b> из списка ниже : '
                                        # f'\nТекущая дата и время <b> /location </b>'
                                        f'\nПриятного пользования'
                          ,reply_markup=markup, parse_mode='html')

@dp.message_handler(commands=['moon'])
async def moonday(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    if timedelta(nameid).strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'): content = content_today
    if timedelta(nameid).strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'): content = content_tomorrow
    if timedelta(nameid).strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'): content = content_yesterday

    moon = content.find('div', class_='firstInfo').find('div', class_='MoonDay') \
                      .find_all(string=lambda text: isinstance(text, Comment))[1].split('DNone">')[1][:-13]

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    await message.answer(               '  🌓   **Лунный прогноз на день** '
                                        f'\n  --------------------------------'
                                        f'\n   {moon}'
                          ,reply_markup=markup, parse_mode='Markdown')

@dp.message_handler(commands=['tibet'])
async def tibet(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    if timedelta(nameid).strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'): content = tibet_today
    if timedelta(nameid).strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'): content = tibet_tomorrow
    if timedelta(nameid).strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'): content = tibet_yesterday

    start = content.find("праздники") + len("праздники")
    end = content.find("Главная")
    holiday = content[start:end]

    if ".Последствия" in content: content = content.replace('.Последствия', ' Последствия')
    if ".Поездка" in content: content = content.replace('.Поездка', ' Поездка')
    if ".Последствия поездки:" in content: content = content.replace('.Последствия поездки:', ' Последствия поездки:')

    start = content.find("Последствия стрижки")  # -- Стрижка --
    end = content.find("Последствия мытья")
    item1 = content[start:end]

    start1 = content.find("Последствия стрижки")
    end1 = content.find(".Местонахождение")
    item2 = content[start1:end1]
    item2 = item2.replace('.Поездка', ' Поездка')

    start2 = content.find("Последствия мытья")  # -- Мытьё --
    end2 = content.find("Последствия стрижки")
    item3 = content[start2:end2]

    start3 = content.find("Последствия мытья")
    end3 = content.find(".Местонахождение")
    item4 = content[start3:end3]
    item4 = item4.replace('.Поездка', ' Поездка')

    start4 = content.find("Последствия поездки:")  # -- Поездка --
    end4 = content.find(".Местонахождение")
    item5 = content[start4:end4]

    start5 = content.find("Поездка")
    end5 = content.find("Последствия стрижки")
    item6 = content[start5:end5]

    start6 = content.find("Поездка")
    end6 = content.find("Последствия мытья")
    item7 = content[start6:end6]

    start7 = content.find("Поездка")
    end7 = content.find(".Местонахождение")
    item8 = content[start7:end7]

    start8 = content.find("Последствия поездки:")
    end8 = content.find("Последствия стрижки")
    item9 = content[start8:end8]

    start9 = content.find("Последствия поездки:")
    end9 = content.find("Последствия мытья")
    item10 = content[start9:end9]

    result1 = ''
    result2 = ''
    result3 = ''
    # ===============  Запрос для стрижки ======================
    if "стрижки" in item1 and "Поездка" not in item1 and "поездки:" not in item1:
        idx_sub_start = item1.find("Последствия стрижки")
        idx_sub_end = item1.find("Последствия мытья")
        result1 = item1[idx_sub_start:idx_sub_end]
        # print(item1[idx_sub_start:idx_sub_end])
        # print('1 Код успешно выполнился')
    elif "Поездка" not in item2 and "поездки:" not in item2:
        result1 = item2
        # print(item2)
        # print('2 Код успешно выполнился')
    elif "Поездка" in item2:
        idx_sub_start = item2.find("Последствия стрижки")
        idx_sub_end = item2.find("Поездка")
        result1 = item2[idx_sub_start:idx_sub_end]
        # print(item2[idx_sub_start:idx_sub_end])
        # print('3 Код успешно выполнился')
    elif "поездки:" in item2:
        idx_sub_start = item2.find("Последствия стрижки")
        idx_sub_end = item2.find("Последствия поездки:")
        result1 = item2[idx_sub_start:idx_sub_end]
        # print(item2[idx_sub_start:idx_sub_end])
        # print('4 Код успешно выполнился')

    # ===============  Запрос для мытья ======================
    if "мытья" in item3:
        idx_sub_start = item3.find("Последствия мытья")
        idx_sub_end = item3.find("Последствия стрижки")
        result2 = item3[idx_sub_start:idx_sub_end]
        # print(item3[idx_sub_start:idx_sub_end])
        # print('1 Код успешно выполнился')
    elif "Поездка" not in item4 and "поездки:" not in item4:
        result2 = item4
        # print(item4)
        # print('2 Код успешно выполнился')
    elif "Поездка" in item4:
        idx_sub_start = item4.find("Последствия мытья")
        idx_sub_end = item4.find("Поездка")
        result2 = item4[idx_sub_start:idx_sub_end]
        # print(item4[idx_sub_start:idx_sub_end])
        # print('3 Код успешно выполнился')
    elif "поездки:" in item4:
        idx_sub_start = item4.find("Последствия мытья")
        idx_sub_end = item4.find("Последствия поездки:")
        result2 = item4[idx_sub_start:idx_sub_end]
        # print(item4[idx_sub_start:idx_sub_end])
        # print('4 Код успешно выполнился')

    # ===============  Поездка ======================
    if "Последствия поездки:" in item5 and "мытья" not in item5 and "стрижки" not in item5:
        result3 = item5
        # print(item5)
        # print('1 Код успешно выполнился')
    elif "Поездка" in item6 and "мытья" not in item6 and "стрижки" not in item6:
        result3 = item6
        # print(item6)
        # print('2 Код успешно выполнился')
    elif "Поездка" in item7 and "мытья" not in item7 and "стрижки" not in item7:
        result3 = item7
        # print(item7)
        # print('3 Код успешно выполнился')
    elif "Поездка" in item8 and "мытья" not in item8 and "стрижки" not in item8:
        result3 = item8
        # print(item8)
        # print('4 Код успешно выполнился')
    elif "Последствия поездки:" in item9 and "мытья" not in item9 and "стрижки" not in item9:
        result3 = item9
        # print(item9)
        # print('5 Код успешно выполнился')
    elif "Последствия поездки:" in item10 and "мытья" not in item10 and "стрижки" not in item10:
        result3 = item10
        # print(item10)
        # print('6 Код успешно выполнился')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    await message.answer(               f'\n  ⛩  <b> Тибетские прогнозы </b>'
                                        f'\n  --------------------------------'
                                        f'\n  🙏  {holiday}'
                                        f'\n  --------------------------------'
                                        f'\n  ✂️  {result1}'
                                        f'\n  --------------------------------'
                                        f'\n  🚿  {result2}'
                                        f'\n  --------------------------------'
                                        f'\n  🛺  {result3}'
                          ,reply_markup=markup, parse_mode='html')

@dp.message_handler(commands=['day'])
async def day(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    if timedelta(nameid).strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'): content = content_today
    if timedelta(nameid).strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'): content = content_tomorrow
    if timedelta(nameid).strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'): content = content_yesterday

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
    await message.answer(               f'\n 📅  <b>Сегодня :   {timedelta(nameid).strftime("%d-%m-%Y")}</b>'
                                        f'\n-------------------------------'
                                        f'\n  - <b><u> {DSymbol}</u></b>'
                                        f'\n   -  {DSymbolo}'
                                        f'\n -------------------------------------'
                                        f'\n  ✅ -  {DayPlus}'
                                        f'\n  ⛔️ -  {DayMinus}'
                                        f'\n -------------------------------------'
                                        f'\n{str(DMoon).strip()}'
                                    ,reply_markup=markup, parse_mode='html')

@dp.message_handler(commands=['stars'])
async def stars(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    if timedelta(nameid).strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'): content = content_today
    if timedelta(nameid).strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'): content = content_tomorrow
    if timedelta(nameid).strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'): content = content_yesterday
    content = content.find('div', class_='firstInfo')
    try:  # Разрушитель года или месяца (Надо подставить слово "Разрушитель")
        collision1 = content.find('h5', class_='red Collision').text  # .split()[-1]
    except:
        collision1 = ''
    try:  # Описание для Разрушителя.
        collision1o = content.findAll('p')[4].text
    except:
        collision1o = ''
    try:  # Второй Разрушитель, если есть первый года или месяца (Надо подставить слово "Разрушитель")
        collision2 = content.findAll('h5', class_='red Collision')[1].text  # .split()[-1]
    except:
        collision2 = ''
    try:  # Описание для Разрушителя.
        collision2o = content.findAll('p')[5].text
    except:
        collision2o = ''
    try:  # Красное ША года
        sha1 = content.find('h5', class_='red Sha').text
    except:
        sha1 = ''
    try:  # Описание для ША
        sha1o = content.find('p', class_='Sha').text
    except:
        sha1o = ''
    try:  # Красное второе ША года
        sha2 = content.findAll('h5', class_='red Sha')[1].text
    except:
        sha2 = ''
    try:  # Описание для ША
        sha2o = content.findAll('p', class_='Sha')[1].text
    except:
        sha2o = ''
    try:  # Позитивный символ для Звезды
        positive1 = content.find('h5', class_='positive SymbolStars').text  # оставить
    except:
        positive1 = ''
    try:  # Описание позитивного символа
        positive1o = content.find('p', class_='SymbolStars').text
    except:
        positive1o = ''
    try:  # Позитивный второй символ для Звезды
        positive2 = content.findAll('h5', class_='positive SymbolStars')[1].text
    except:
        positive2 = ''
    try:  # Описание второго позитивного символа
        positive2o = content.findAll('p', class_='SymbolStars')[2].text
    except:
        positive2o = ''
    try:  # Символ MKD
        symbolMKD = content.find('div', class_='SymbolStars MKD').text
    except:
        symbolMKD = ''
    try:  # Негативный символ для Звезды
        negative = content.find('h5', class_='negative SymbolStars').text
    except:
        negative = ''
    try:  # Описание негативного символа
        negativeo = content.findAll('p', class_='SymbolStars')[1].text
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
        await message.answer(f'\n ⭐️<b><u> Cимволы дня и летящие звёзды </u></b>'
                                         f'\n---------------------------------------'
                                         f'\n Сегодня нет информации'
                                    ,reply_markup=markup, parse_mode='html')
    else:
        await message.answer(
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
            ,reply_markup=markup, parse_mode='html')

@dp.message_handler(commands=['hour'])
async def daytimes(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    if timedelta(nameid).strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'): content = content_today
    if timedelta(nameid).strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'): content = content_tomorrow
    if timedelta(nameid).strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'): content = content_yesterday

    DayHour = ''
    Animals = ''
    try:
        if timedelta(nameid).time() >= datetime.time(23, 1) \
                and timedelta(nameid).time() <= datetime.time(23, 59):
            DayHour = content.findAll('td')[-1]
            Animals = 'Час Крысы 🐁 с 23:00 до 01:00'
        elif timedelta(nameid).time() >= datetime.time(21, 1) \
                and timedelta(nameid).time() <= datetime.time(23, 00):
            DayHour = content.findAll('td')[-2]
            Animals = 'Час Свиньи 🐖 с 21:00 до 23:00'
        elif timedelta(nameid).time() >= datetime.time(19, 1) \
                and timedelta(nameid).time() <= datetime.time(21, 00):
            DayHour = content.findAll('td')[-3]
            Animals = 'Час Собаки 🐕 с 19:00 до 21:00'
        elif timedelta(nameid).time() >= datetime.time(17, 1) \
                and timedelta(nameid).time() <= datetime.time(19, 00):
            DayHour = content.findAll('td')[-4]
            Animals = 'Час Петуха 🐓 с 17:00 до 19:00'
        elif timedelta(nameid).time() >= datetime.time(15, 1) \
                and timedelta(nameid).time() <= datetime.time(17, 00):
            DayHour = content.findAll('td')[-5]
            Animals = 'Час Обезьяны 🐒 с 15:00 до 17:00'
        elif timedelta(nameid).time() >= datetime.time(13, 1) \
                and timedelta(nameid).time() <= datetime.time(15, 00):
            DayHour = content.findAll('td')[-6]
            Animals = 'Час Козы 🐐 с 13:00 до 15:00'
        elif timedelta(nameid).time() >= datetime.time(11, 1) \
                and timedelta(nameid).time() <= datetime.time(13, 00):
            DayHour = content.findAll('td')[-7]
            Animals = 'Час Лошади 🐎 с 11:00 до 13:00'
        elif timedelta(nameid).time() >= datetime.time(9, 1) \
                and timedelta(nameid).time() <= datetime.time(11, 00):
            DayHour = content.findAll('td')[-8]
            Animals = 'Час Змеи 🐍 с 09:00 до 11:00'
        elif timedelta(nameid).time() >= datetime.time(7, 1) \
                and timedelta(nameid).time() <= datetime.time(9, 00):
            DayHour = content.findAll('td')[-9]
            Animals = 'Час Дракона 🐉 с 07:00 до 09:00'
        elif timedelta(nameid).time() >= datetime.time(5, 1) \
                and timedelta(nameid).time() <= datetime.time(7, 00):
            DayHour = content.findAll('td')[-10]
            Animals = 'Час Кролика 🐇 с 05:00 до 07:00'
        elif timedelta(nameid).time() >= datetime.time(3, 1) \
                and timedelta(nameid).time() <= datetime.time(5, 00):
            DayHour = content.findAll('td')[-11]
            Animals = 'Час Тигра 🐅 с 03:00 до 05:00'
        elif timedelta(nameid).time() >= datetime.time(1, 1) \
                and timedelta(nameid).time() <= datetime.time(3, 00):
            DayHour = content.findAll('td')[-12]
            Animals = 'Час Быка 🐂 с 01:00 до 03:00'
        elif timedelta(nameid).time() >= datetime.time(0, 00) \
                and timedelta(nameid).time() <= datetime.time(1, 00):
            DayHour = content.findAll('td')[-13]
            Animals = 'Час Крысы 🐁 с 23:00 до 01:00'
    except:
        DayHour = ''

    try: # Пробую получить информацию
        plus_minus = DayHour.findAll('p', class_='PlusMinus')
    except:
        plus_minus = ''
    try:  # Пробую получить информацию
        plus_minuso = DayHour.find('p', class_='PlusMinus').text
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
        Collision = DayHour.find('p', class_='Collision').text
    except:
        Collision = ''
    try:
        SymbolStars = DayHour.findAll('p', class_='SymbolStars')[0].text
    except:
        SymbolStars = ''
    try:
        SymbolStars1 = DayHour.findAll('p', class_='SymbolStars')[1].text
    except:
        SymbolStars1 = ''
    try:
        SymbolStars2 = DayHour.findAll('p', class_='SymbolStars')[2].text
    except:
        SymbolStars2 = ''
    try:
        SymbolStars3 = DayHour.findAll('p', class_='SymbolStars')[3].text
    except:
        SymbolStars3 = ''

    if Positive: Positive = '\n ✅  ' + plus_minuso.strip()
    if Negative: Negative = '\n ⛔️  ' + plus_minuso.strip()
    if Negative2: Negative2 = '\n ⛔️  ' + plus_minus[1].text.strip()
    if Collision: Collision = '\n ➖  ' + Collision.strip()
    if SymbolStars: SymbolStars = '\n 🛟 ' + SymbolStars
    if SymbolStars1: SymbolStars1 = '\n 🔮 ' + SymbolStars1
    if SymbolStars2: SymbolStars2 = '\n 🧿 ' + SymbolStars2
    if SymbolStars3: SymbolStars3 = '\n 🔑 ' + SymbolStars3

    Negative1 = str(Negative).strip()
    Positive1 = str(Positive).strip()

    ours = Negative1+Positive1

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))

    if not ours:
        await message.answer(
                         f'\n 🕒<b>  Сейчас {timedelta(nameid).strftime("%H:%M")} -- {Animals}</b>'
                         f'\n'
                         f'\n Нет информации на текущее время.'
                         f'\n Попробуйте посмотреть через час.'
            ,reply_markup=markup, parse_mode='html')
    else:
        await message.answer(
                         f'\n 🕒<b>  Сейчас {timedelta(nameid).strftime("%H:%M")} '
                         f'\n{Animals}</b>'
                         f'\n--------------------------------------'
                         f' {f"{Positive}" if Positive else ""}'
                         f' {f"{Negative}" if Negative else ""}'
                         f' {f"{Negative2}" if Negative2 else ""}'
                         f'\n<b>----------+++----------</b>'
                         f' {f"{Collision}" if Collision else ""}'
                         f' {f"{SymbolStars}" if SymbolStars else ""}'
                         f' {f"{SymbolStars1}" if SymbolStars1 else ""}'
                         f' {f"{SymbolStars2}" if SymbolStars2 else ""}'
                         f' {f"{SymbolStars3}" if SymbolStars3 else ""}'
                         ,reply_markup=markup, parse_mode='html')

@dp.message_handler(commands=['hours'])
async def allhours(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    if timedelta(nameid).strftime('%d-%m-%Y') == get_today().strftime('%d-%m-%Y'): content = content_today
    if timedelta(nameid).strftime('%d-%m-%Y') == get_tomorrow().strftime('%d-%m-%Y'): content = content_tomorrow
    if timedelta(nameid).strftime('%d-%m-%Y') == get_yesterday().strftime('%d-%m-%Y'): content = content_yesterday

    items = []
    for p in range(-13, 0):
        try:
            item1 = content.findAll('div', class_='HourTime')[p].text  # Это для час
        except:
            item1 = ''
        # ============================= Тут описание =======================================
        DayHour = content.findAll('td')[p]
        try:  # Пробую получить информацию
            plus_minus = DayHour.findAll('p', class_='PlusMinus')
        except:
            plus_minus = ''
        try:  # Пробую получить информацию
            plus_minuso = DayHour.find('p', class_='PlusMinus').text
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

        if Positive: Positive = '\n ✅  ' + plus_minuso.strip()
        if Negative: Negative = '\n ⛔️  ' + plus_minuso.strip()
        if Negative2: Negative2 = '\n ⛔️  ' + plus_minus[1].text.strip()

        # items.append(f'{item1}\n{f"{Positive}" if Positive else ""}\n{f"{Negative}" if Negative else ""}\n{f"{Negative2}" if Negative2 else ""}')
        items.append(f'{item1}\n{Positive}\n{Negative}\n{Negative2}')

    result = [x.strip().replace('\xa0', ' ') for x in items]
    result = [x.strip().replace('None', '') for x in result]
    result = [x.strip().replace('\n', '') for x in result]
    result = '\n'.join(result)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    await message.answer(               '  🧭   **Все двухчасовки на сегодня** '
                                        f'\n  --------------------------------'
                                        f'\n{result}'
                          ,reply_markup=markup, parse_mode='Markdown')




# ========================================================================================================
#                       Обработка  Запросов  Callback
# ========================================================================================================
@dp.callback_query_handler()
async def callback(call):
    global content_today, content_yesterday, content_tomorrow

    if call.data == 'Ukr':
        db_path = os.path.join("db", "userdata.sql")
        nameid = call.from_user.id
        usertime = call.message.date
        conn = sqlite3.connect(db_path)
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
        await bot.send_message(call.message.chat.id, f'Вы выбрали Украина 🇺🇦 UTC+2\n{timedelta}')

    elif call.data == 'Pol':
        db_path = os.path.join("db", "userdata.sql")
        nameid = call.from_user.id
        usertime = call.message.date
        conn = sqlite3.connect(db_path)
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
        await bot.send_message(call.message.chat.id, f'Вы выбрали Польша 🇵🇱 UTC+1\n{timedelta}')

    elif call.data == 'Usa':
        db_path = os.path.join("db", "userdata.sql")
        nameid = call.from_user.id
        usertime = call.message.date
        conn = sqlite3.connect(db_path)
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
        await bot.send_message(call.message.chat.id, f'Вы выбрали США 🇺🇸 UTC-4\n{timedelta}')

    elif call.data == 'back':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('⛩  Тибетский прогноз на сегодня', callback_data='tibet')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('📅  Китайский прогноз на сегодня', callback_data='today')
        markup.row(btn2)
        btn3 = types.InlineKeyboardButton('🌓 Лунный день', callback_data='moon')
        btn4 = types.InlineKeyboardButton('️️⭐️  Звёзды', callback_data='stars')
        markup.row(btn3, btn4)
        btn5 = types.InlineKeyboardButton('🧭 Все часы', callback_data='hours')
        btn6 = types.InlineKeyboardButton('❓ Помощь', callback_data='help')
        markup.row(btn5, btn6)
        await bot.edit_message_text(text=   f'\n💡  <b>Меню</b>'
                                            f'\n  ------------'
                                            f'\n  Быстрое использование всех команд бота.'
                                            f'\n- Прогноз на день или на час по китайскому календарю.'
                                            f'\n- Тибетский прогноз (праздники, стрижка, поездки)'
                                            f'\n- Лунный прогноз на день'
                                            f'\n- Что говорят звёзды на сегодня'
                                            f'\n- Вывод справочной информации.'
            ,chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='html', reply_markup=markup)

    elif call.data == 'help':
        await help(call.message)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'today':
        nameid = call.from_user.id
        message = types.Message(chat=types.Chat(id=call.message.chat.id), message_id=call.message.message_id)
        await day(message, nameid)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'tibet':
        nameid = call.from_user.id
        message = types.Message(chat=types.Chat(id=call.message.chat.id), message_id=call.message.message_id)
        await tibet(message, nameid)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'moon':
        nameid = call.from_user.id
        message = types.Message(chat=types.Chat(id=call.message.chat.id), message_id=call.message.message_id)
        await moonday(message, nameid)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'stars':
        nameid = call.from_user.id
        message = types.Message(chat=types.Chat(id=call.message.chat.id), message_id=call.message.message_id)
        await stars(message, nameid)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'hour':
        nameid = call.from_user.id
        message = types.Message(chat=types.Chat(id=call.message.chat.id), message_id=call.message.message_id)
        await daytimes(message, nameid)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'hours':
        nameid = call.from_user.id
        message = types.Message(chat=types.Chat(id=call.message.chat.id), message_id=call.message.message_id)
        await allhours(message, nameid)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

# ========================================================================================================
#                       Тут  Callback  Закончился  :))
# ========================================================================================================

#============================ Вывод запроса на дату =========================
@dp.message_handler(content_types=['text'])
async def fordate(message):
    waitfor = await bot.send_message(message.chat.id, 'Ожидайте загрузки ... ⌛️')
    date_str = message.text.strip().lower()
    try:
        date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y')
    except ValueError:
        await bot.edit_message_text(text=f'Дата указана не верно',chat_id=waitfor.chat.id, message_id=waitfor.message_id)
        return
    content = StarsDay(date_str)  # Запрос на выгрузку контента согласно введённой дате
    content_tibet = TibetHolly(date_str)  # Запрос на выгрузку контента согласно введённой дате

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

    # ================================== Звёзды ===========================================

    content = content.find('div', class_='firstInfo')
    try:  # Разрушитель года или месяца (Надо подставить слово "Разрушитель")
        collision1 = content.find('h5', class_='red Collision').text  # .split()[-1]
    except:
        collision1 = ''
    try:  # Описание для Разрушителя.
        collision1o = content.findAll('p')[4].text
    except:
        collision1o = ''
    try:  # Второй Разрушитель, если есть первый года или месяца (Надо подставить слово "Разрушитель")
        collision2 = content.findAll('h5', class_='red Collision')[1].text  # .split()[-1]
    except:
        collision2 = ''
    try:  # Описание для Разрушителя.
        collision2o = content.findAll('p')[5].text
    except:
        collision2o = ''
    try:  # Красное ША года
        sha1 = content.find('h5', class_='red Sha').text
    except:
        sha1 = ''
    try:  # Описание для ША
        sha1o = content.find('p', class_='Sha').text
    except:
        sha1o = ''
    try:  # Красное второе ША года
        sha2 = content.findAll('h5', class_='red Sha')[1].text
    except:
        sha2 = ''
    try:  # Описание для ША
        sha2o = content.findAll('p', class_='Sha')[1].text
    except:
        sha2o = ''
    try:  # Позитивный символ для Звезды
        positive1 = content.find('h5', class_='positive SymbolStars').text  # оставить
    except:
        positive1 = ''
    try:  # Описание позитивного символа
        positive1o = content.find('p', class_='SymbolStars').text
    except:
        positive1o = ''
    try:  # Позитивный второй символ для Звезды
        positive2 = content.findAll('h5', class_='positive SymbolStars')[1].text
    except:
        positive2 = ''
    try:  # Описание второго позитивного символа
        positive2o = content.findAll('p', class_='SymbolStars')[2].text
    except:
        positive2o = ''
    try:  # Символ MKD
        symbolMKD = content.find('div', class_='SymbolStars MKD').text
    except:
        symbolMKD = ''
    try:  # Негативный символ для Звезды
        negative = content.find('h5', class_='negative SymbolStars').text
    except:
        negative = ''
    try:  # Описание негативного символа
        negativeo = content.findAll('p', class_='SymbolStars')[1].text
    except:
        negativeo = ''

    stars = collision1.strip() + collision1o + collision2.strip() + collision2o + sha1 + sha1o.strip() + sha2 + sha2o.strip() \
            + positive1 + positive1o + positive2 + positive2o + symbolMKD + negative + negativeo

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

    # ================================== Информация по Тибету ===========================================

    start = content_tibet.find("праздники") + len("праздники")
    end = content_tibet.find("Главная")
    holiday = content_tibet[start:end]

    if ".Последствия" in content_tibet: content_tibet = content_tibet.replace('.Последствия', ' Последствия')
    if ".Поездка" in content_tibet: content_tibet = content_tibet.replace('.Поездка', ' Поездка')
    if ".Последствия поездки:" in content_tibet: content_tibet = content_tibet.replace('.Последствия поездки:', ' Последствия поездки:')

    start = content_tibet.find("Последствия стрижки")  # -- Стрижка --
    end = content_tibet.find("Последствия мытья")
    item1 = content_tibet[start:end]

    start1 = content_tibet.find("Последствия стрижки")
    end1 = content_tibet.find(".Местонахождение")
    item2 = content_tibet[start1:end1]
    item2 = item2.replace('.Поездка', ' Поездка')

    start2 = content_tibet.find("Последствия мытья")  # -- Мытьё --
    end2 = content_tibet.find("Последствия стрижки")
    item3 = content_tibet[start2:end2]

    start3 = content_tibet.find("Последствия мытья")
    end3 = content_tibet.find(".Местонахождение")
    item4 = content_tibet[start3:end3]
    item4 = item4.replace('.Поездка', ' Поездка')

    start4 = content_tibet.find("Последствия поездки:")  # -- Поездка --
    end4 = content_tibet.find(".Местонахождение")
    item5 = content_tibet[start4:end4]

    start5 = content_tibet.find("Поездка")
    end5 = content_tibet.find("Последствия стрижки")
    item6 = content_tibet[start5:end5]

    start6 = content_tibet.find("Поездка")
    end6 = content_tibet.find("Последствия мытья")
    item7 = content_tibet[start6:end6]

    start7 = content_tibet.find("Поездка")
    end7 = content_tibet.find(".Местонахождение")
    item8 = content_tibet[start7:end7]

    start8 = content_tibet.find("Последствия поездки:")
    end8 = content_tibet.find("Последствия стрижки")
    item9 = content_tibet[start8:end8]

    start9 = content_tibet.find("Последствия поездки:")
    end9 = content_tibet.find("Последствия мытья")
    item10 = content_tibet[start9:end9]

    result1 = ''
    result2 = ''
    result3 = ''
    # ===============  Запрос для стрижки ======================
    if "стрижки" in item1 and "Поездка" not in item1 and "поездки:" not in item1:
        idx_sub_start = item1.find("Последствия стрижки")
        idx_sub_end = item1.find("Последствия мытья")
        result1 = item1[idx_sub_start:idx_sub_end]
    elif "Поездка" not in item2 and "поездки:" not in item2:
        result1 = item2
    elif "Поездка" in item2:
        idx_sub_start = item2.find("Последствия стрижки")
        idx_sub_end = item2.find("Поездка")
        result1 = item2[idx_sub_start:idx_sub_end]
    elif "поездки:" in item2:
        idx_sub_start = item2.find("Последствия стрижки")
        idx_sub_end = item2.find("Последствия поездки:")
        result1 = item2[idx_sub_start:idx_sub_end]

    # ===============  Запрос для мытья ======================
    if "мытья" in item3:
        idx_sub_start = item3.find("Последствия мытья")
        idx_sub_end = item3.find("Последствия стрижки")
        result2 = item3[idx_sub_start:idx_sub_end]
    elif "Поездка" not in item4 and "поездки:" not in item4:
        result2 = item4
    elif "Поездка" in item4:
        idx_sub_start = item4.find("Последствия мытья")
        idx_sub_end = item4.find("Поездка")
        result2 = item4[idx_sub_start:idx_sub_end]
    elif "поездки:" in item4:
        idx_sub_start = item4.find("Последствия мытья")
        idx_sub_end = item4.find("Последствия поездки:")
        result2 = item4[idx_sub_start:idx_sub_end]


    # ===============  Поездка ======================
    if "Последствия поездки:" in item5 and "мытья" not in item5 and "стрижки" not in item5:
        result3 = item5
    elif "Поездка" in item6 and "мытья" not in item6 and "стрижки" not in item6:
        result3 = item6
    elif "Поездка" in item7 and "мытья" not in item7 and "стрижки" not in item7:
        result3 = item7
    elif "Поездка" in item8 and "мытья" not in item8 and "стрижки" not in item8:
        result3 = item8
    elif "Последствия поездки:" in item9 and "мытья" not in item9 and "стрижки" not in item9:
        result3 = item9
    elif "Последствия поездки:" in item10 and "мытья" not in item10 and "стрижки" not in item10:
        result3 = item10

    # ================================== Конец блока по Тибету ===========================================

    await bot.edit_message_text(text=f'\n 🗓  <b>Запрос на дату :   {date_str}</b>'
                                     f'\n-------------------------------'
                                     f'\n  - <b><u> {DSymbol}</u></b>'
                                     f'\n   -  {DSymbolo}'
                                     f'\n -------------------------------------'
                                     f'\n  ✅ -  {DayPlus}'
                                     f'\n  ⛔️ -  {DayMinus}'
                                     f'\n -------------------------------------'
                                     f'\n{str(DMoon).strip()}'
                                , chat_id=waitfor.chat.id, message_id=waitfor.message_id, parse_mode='html')

    if not stars:
        await message.answer(f'\n ⭐️<b><u> Cимволы дня и летящие звёзды </u></b>'
                             f'\n---------------------------------------'
                             f'\n Сегодня нет информации'
                             , parse_mode='html')
    else:
        await message.answer(
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
            , parse_mode='html')

    await message.answer(f'\n  ⛩  <b> Тибетские прогнозы </b>'
                         f'\n  --------------------------------'
                         f'\n  🙏  {holiday}'
                         f'\n  --------------------------------'
                         f'\n  ✂️  {result1}'
                         f'\n  --------------------------------'
                         f'\n  🚿  {result2}'
                         f'\n  --------------------------------'
                         f'\n  🛺  {result3}'
                         , parse_mode='html')



# if __name__ == '__main__':
#     yesterday = get_yesterday()
#     MoonDay(yesterday)
#     today = get_today()
#     MoonDay(today)
#     tomorrow = get_tomorrow()
#     MoonDay(tomorrow)
#     Printersimbols()

file_handler.close()
executor.start_polling(dp)