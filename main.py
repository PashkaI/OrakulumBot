import telebot
import webbrowser
from telebot import types
import datetime
from mingli import Parsi

bot = telebot.TeleBot('6024265589:AAEAsVOB-0w-IaeoS3Ach9bZxLxlg9U7MOo')
my_object = Parsi()

@bot.message_handler(commands=['start', 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, <b>{message.from_user.first_name}.</b> '
                                      f'\nТвой ID: , {message.from_user.id} '
                                      f'\nДля получения справки введи команду <b> /help </b>'
                                      f'\nГлавное меню <b> /main </b>'
                                      f'\nПрогноз на день <b> /day </b>'
                                      f'\nПрогноз на Час <b> /hour </b>'
                                      f'\nЛунный прогноз на день <b> /moon </b>'
                                      f'\nCимволы дня и летящие звёзды <b> /stars </b>'
                                      f'\nПрофиль пользователя <b> /profile </b>'
                                      f'\nТекущая дата и время <b> /time </b>'
                     ,parse_mode='html')


@bot.message_handler(commands=['main'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('📅  Показать прогноз на сегодня', callback_data='today')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('🌓 Лунный День', callback_data='moon')
    btn3 = types.InlineKeyboardButton('️️⭐️  Звёзды', callback_data='stars')
    markup.row(btn2, btn3)
    btn4 = types.InlineKeyboardButton('🔎  На час', callback_data='hour')
    btn5 = types.InlineKeyboardButton('❓ Помощь', callback_data='help')
    markup.row(btn4, btn5)

    bot.send_message(message.chat.id, f'\n💡  <b>Меню</b>'
                                      f'\n  ------------'
                                      f'\n  Быстрое использование всех команд бота.'
                                      f'\nПрогноз на день или на час по китайскому календарю.'
                                      f' Показать лунный прогноз на день и узнать символ дня.'
                                      f'\nВывод справичной информации.'

                                    ,reply_markup=markup, parse_mode='html')

@bot.callback_query_handler(func=lambda callback: True) # Обработка Запросов Callback =====================================================
def callback_message(callback):
    if callback.data == 'today':
        today(callback.message)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        # params = my_object.pfind(params_needed=['DSymbol', 'DSymbolo', 'DayPlus', 'DayMinus', 'DMoon'])
        # DSymbol = str(params[0]).strip()
        # DSymbolo = str(params[1]).strip()
        # DayPlus = str(params[2]).strip()
        # DayMinus = str(params[3]).strip()
        # DMoon = str(params[4]).strip()
        #
        # markup = types.InlineKeyboardMarkup()
        # btn1 = types.InlineKeyboardButton('↩️  Назад', callback_data='back')
        # btn2 = types.InlineKeyboardButton('🔎  На Час', callback_data='hour')
        # markup.row(btn1, btn2)
        # bot.edit_message_text(          f'\n  - 📅 <b>Сегодня :   {datetime.datetime.now().strftime("%d")}-{datetime.datetime.now().strftime("%m")}-{datetime.datetime.now().strftime("%Y")}</b>'
        #                                 f'\n  - <b><u> {DSymbol}</u></b>'
        #                                 f'\n   -  {DSymbolo}'
        #                                 f'\n  -------------------------------------'
        #                                 f'\n  ✅ -  {DayPlus}'
        #                                 f'\n  ⛔️ -  {DayMinus}'
        #                                 f'\n  -------------------------------------'
        #                                 f'\n{DMoon}'
        #                  ,callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)


    elif callback.data == 'back':
        # main(callback.message)
        # bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('📅  Показать прогноз на сегодня', callback_data='today')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('🌓 Лунный День', callback_data='moon')
        btn3 = types.InlineKeyboardButton('️️⭐️  Звёзды', callback_data='stars')
        markup.row(btn2, btn3)
        btn4 = types.InlineKeyboardButton('🔎  На час', callback_data='hour')
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
        #moonday(callback.message)

        # params = my_object.pfind(params_needed=['moonday'])
        # markup = types.InlineKeyboardMarkup()
        # markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
        # bot.edit_message_text(          f'\n  🌓 <b><u> Прогноз Луны </u></b>'
        #                                 f'\n   {params}'
        #                  ,callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup)

#======================================Конец блока для CallBack ========================================================

@bot.message_handler(commands=['moon'])
def moonday(message):
    waitfor = bot.send_message(message.chat.id, 'Ожидайте загрузки ... ⌛️')
    params = my_object.pfind(params_needed=['moonday'])
    #moon = str(params[0]).strip()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('↩️  Назад', callback_data='back'))
    bot.edit_message_text(              f'\n  🌓 <b> Лунный прогноз на день </b>'
                                        f'\n  --------------------------------'
                                        f'\n   {params}'
                          ,chat_id=waitfor.chat.id, message_id=waitfor.message_id, reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['time'])
def send_welcome(message):
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") # получаем текущую дату и время и форматируем ее в строку
    bot.reply_to(message, f"Текущая дата и время: {current_time}") # отправляем сообщение с текущей датой и временем

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
                                        f'\nCимволы дня и летящие звёзды <b> /stars </b>'
                                        f'\nПрофиль пользователя <b> /profile </b>'
                                        f'\nТекущая дата и время <b> /time </b>'
                                        f'\n'
                                        f'\n🔹  <b>Что умеет этот бот:</b>'
                                        f'\n'
                                        f'\nРобот выводит прогноз на день или на час по китайскому календарю.'
                                        f' А так же можно посмотреть лунный прогноз на день и символ дня.'
                                        f' В будущем возможно ещё сделаю вывод информации по Тибетским праздникам.'
                                        f'\n'
                                        f'\nПо работе бота писать: @Rts_support'
                          ,reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://google.com')


@bot.message_handler(commands=['day'])
def today(message):
    waitfor = bot.send_message(message.chat.id, 'Ожидайте загрузки ... ⌛️')
    params = my_object.pfind(params_needed=['Content'])
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

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('↩️  Назад', callback_data='back')
    btn2 = types.InlineKeyboardButton('🔎  На Час', callback_data='hour')
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
    params = my_object.pfind(params_needed=['Content'])
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
    params = my_object.pfind(params_needed=['DayHour'])
    animails = my_object.pfind(params_needed=['Animals'])
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


bot.polling(none_stop=True)