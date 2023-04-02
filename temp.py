
from mingli import Parsi


def moonday():
    my_object = Parsi()
    params = my_object.pfind(params_needed=['moonday'])
    print(params)

def today():
    my_object = Parsi()
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

    print(DSymbol)
    print(DSymbolo)
    print(DayPlus)
    print(DayMinus)
    print(DMoon)

def stars():
    my_object = Parsi()
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

    #stars = [s.replace('\n', '') for s in collision1 and collision1o and collision2 and  if s.strip()]
    stars = collision1.strip()+collision1o+collision2.strip()+collision2o+sha1+sha1o.strip()+sha2+sha2o.strip()\
            +positive1+positive1o+positive2+positive2o+symbolMKD+negative+negativeo

    if not stars:
        print('Нет информации сегодня для звёзд')
    else:
        if collision1: print(f"- {collision1.strip()}")
        #print(f"----" if collision1o.strip() == positive1o.strip() and collision1o.strip() != '' else f"{collision1o.strip()}")
        if collision1: print(f"- {collision1o}")
        if collision2: print(f"- {collision2.strip()}")
        if collision2o and collision2 and collision2o != sha1o: print(f"- {collision2o}")
        if sha1: sha1 = '\n' + sha1.strip()
        print(sha1)
        if sha1o.strip() and not sha2: print(f"- {sha1o.strip()}")
        #print(f"- {sha1o.strip()}" if sha1o.strip() == sha2o.strip() and sha1o.strip() != '' else "")
        if sha2: print(f"- {sha2}")
        if not sha1o.strip() and sha2o.strip() : print(f"- {sha2o.strip()}")
        if sha2o and sha2 and sha2o.strip() == sha1o.strip(): print(f"- {sha2o.strip()}")
        if positive1: print(f"- {positive1}")
        if positive1o and positive1 and positive1o[:-1] != negativeo: print(f"- {positive1o}")
        if positive2: print(f"- {positive2}")
        if positive2o: print(f"- {positive2o}")
        if symbolMKD: print(f"- {symbolMKD}")
        if negative: print(f"- {negative}")
        if negativeo: print(f"- {negativeo}")
        if not negativeo and negative: print(f"- {collision1o}")

    print('=====================================================================================')
    print('collision1', collision1.strip())
    print('collision1o', collision1o)
    print('collision2', collision2.strip())
    print('collision2o', collision2o)
    print('sha1', sha1)
    print('sha1o', sha1o.strip())
    print('sha2', sha2)
    print('sha2o', sha2o.strip())
    print('positive1', positive1)
    print('positive1o', positive1o)
    print('positive2', positive2)
    print('positive2o', positive2o)
    print('symbolMKD', symbolMKD)
    print('negative', negative)
    print('negativeo', negativeo)


def DayTimes():
    my_object = Parsi()
    params = my_object.pfind(params_needed=['DayHour'])
    animals = my_object.pfind(params_needed=['Animals'])
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

    # ==========================================================================================
    # if plus_minus:
    #     dhourPlus = plus_minus[0].find('span', class_='IconPositive')
    #     if dhourPlus:
    #         pluso = '\n' + plus_minuso
    #     else:
    #         pluso = ''
    #
    #     dhourMinus = plus_minus[0].find('span', class_='IconNegative')
    #     if dhourMinus:
    #         minuso = '\n' + plus_minuso
    #     else:
    #         minuso = ''
    #     ###===========Второй Блок =============
    #     try:
    #         dhourMinus1 = plus_minus[1].find('span', class_='IconNegative')
    #     except:
    #         dhourMinus1 = ''
    #     if dhourMinus1:
    #         minuso2 = '\n' + plus_minus[1].text
    #     else:
    #         minuso2 = ''
    # ==========================================================================================

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

    if Positive: Positive = '\n ✅ - Positive' + plus_minuso.strip()
    if Negative: Negative = '\n ⛔️ - Negative' + plus_minuso.strip()
    if Negative2: Negative2 = '\n ⛔️ - Negative' + plus_minus[1].text.strip()
    if Collision: Collision = '\n Collision - ' + Collision
    if SymbolStars: SymbolStars = '\n SymbolStars - ' + SymbolStars
    if SymbolStars1: SymbolStars1 = '\n SymbolStars1 - ' + SymbolStars1
    if SymbolStars2: SymbolStars2 = '\n SymbolStars2 - ' + SymbolStars2
    if SymbolStars3: SymbolStars3 = '\n SymbolStars3 - ' + SymbolStars3

    print(params)
    print(animals)


    # print(Positive)
    # print(Negative)
    # print(Negative2)
    #
    # print(Collision)
    # print(SymbolStars)
    # print(SymbolStars1)
    # print(SymbolStars2)
    # print(SymbolStars3)



DayTimes()