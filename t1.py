
import datetime
import requests
from bs4 import BeautifulSoup, Comment


def today():
    base_url = "eyJjaXR5Ijp7ImNpdHkiOiJcdTA0MmRcdTA0M2JcdTA0M2EiLCJjaXR5aWQiOiI4MDM1NyIsInV0YyI6IisxLjAiLCJzdXRjIjoxLCJsbmciOiIyMi4zNjQ2NjI5IiwibGF0IjoiNTMuODI4MDUyOSIsInR6IjoiRXVyb3BlXC9XYXJzYXciLCJnb29nbGVfaWQiOiJDaElKQi1OaE4zLTU0VVlSWWtHQ0ZHb0dRVk0iLCJnZW9uYW1laWQiOiI3NzI2MjEiLCJ1YXV0byI6MX0sInBybyI6IjAiLCJIb3Vyc1R5cGUiOiIwIn0="
    current_dtime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    current_year = datetime.datetime.now().strftime("%Y")
    current_month = datetime.datetime.now().strftime("%m")
    current_date = datetime.datetime.now().strftime("%d")
    current_time = datetime.datetime.now().strftime("%H:%M")
    url = f"https://www.mingli.ru/24-3-{current_year}/{base_url}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    # =============================== Хороший код==для + - на часе =================================
    param = soup.find('div', class_='Content').findAll('td')[-5]
    plus_minus = param.findAll('p', class_='PlusMinus')
    plus_minuso = param.find('p', class_='PlusMinus').text

    if plus_minus:
        dhourPlus = plus_minus[0].find('span', class_='IconPositive')
        if dhourPlus:
            dhourPlus = dhourPlus.get('title')
            print(f'\n Позитивная информация - {dhourPlus} \n {plus_minuso}')
        else:
            print("\n Нет информации о позитивных делах")

        dhourMinus = plus_minus[0].find('span', class_='IconNegative')
        if dhourMinus:
            dhourMinus = dhourMinus.get('title')
            print(f'\n Негативная информация - {dhourMinus} \n {plus_minuso}')
        else:
            print("\n Нет информации о негативных делах в теге 0")
        ###===========Второй Блок =============
        try:
            dhourMinus1 = plus_minus[1].find('span', class_='IconNegative')
        except:
            dhourMinus1 = ''
        if dhourMinus1:
            dhourMinus1 = dhourMinus1.get('title')
            print(f'\n Негативная информация - {dhourMinus1} \n {plus_minus[1].text}')
    # ==========================================================================================

    try:
        param1 = param.find('p', class_='Collision').text
    except:
        param1 = ''

    try:
        param2 = param.findAll('p', class_='SymbolStars')[0].text
    except:
        param2 = ''
    try:
        param3 = param.findAll('p', class_='SymbolStars')[1].text
    except:
        param3 = ''
    try:
        param4 = param.findAll('p', class_='SymbolStars')[2].text
    except:
        param4 = ''
    try:
        param5 = param.findAll('p', class_='SymbolStars')[3].text
    except:
        param5 = ''

    print(param)
    # print(param1)
    # print(param2)
    # print(param3)
    # print(param4)
    # print(param5)




today()