import datetime
import requests
from bs4 import BeautifulSoup, Comment
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
def get_today():
    return datetime.date.today()

today = get_today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

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
    if data_url == today:
        moon_today = moon
    elif data_url == yesterday:
        moon_yesterday = moon
    elif data_url == tomorrow:
        moon_tomorrow = moon
    return moon

scheduler.add_job(MoonDay, 'cron', hour=11, minute=37, second=20, args=[today])
scheduler.add_job(MoonDay, 'cron', hour=11, minute=37, second=30, args=[yesterday])
scheduler.add_job(MoonDay, 'cron', hour=11, minute=37, second=40, args=[tomorrow])
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

while True:
    continue
