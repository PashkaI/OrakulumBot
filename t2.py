
import datetime
import requests
from bs4 import BeautifulSoup


def today():
    base_url = "eyJjaXR5Ijp7ImNpdHkiOiJcdTA0MmRcdTA0M2JcdTA0M2EiLCJjaXR5aWQiOiI4MDM1NyIsInV0YyI6IisxLjAiLCJzdXRjIjoxLCJsbmciOiIyMi4zNjQ2NjI5IiwibGF0IjoiNTMuODI4MDUyOSIsInR6IjoiRXVyb3BlXC9XYXJzYXciLCJnb29nbGVfaWQiOiJDaElKQi1OaE4zLTU0VVlSWWtHQ0ZHb0dRVk0iLCJnZW9uYW1laWQiOiI3NzI2MjEiLCJ1YXV0byI6MX0sInBybyI6IjAiLCJIb3Vyc1R5cGUiOiIwIn0="
    current_dtime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    current_year = datetime.datetime.now().strftime("%Y")
    current_month = datetime.datetime.now().strftime("%m")
    current_date = datetime.datetime.now().strftime("%d")
    current_time = datetime.datetime.now().strftime("%H:%M")

    data = []
    for p in range(1, 32):
        print(p)
        url = f"https://www.mingli.ru/{p}-{current_month}-{current_year}/{base_url}"
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        main = soup.find('div', class_='Content').findAll('div', class_='firstInfo')

        for simbol in main:
            try:
                item1 = simbol.find('h5', class_='red Collision').text
            except:
                item1 = ''
            try:
                item2 = simbol.findAll('h5', class_='red Collision')[1].text
            except:
                item2 = ''
            data.append([item1, item2])

    print(data)
today()