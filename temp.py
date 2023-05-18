import requests

# Создание сеанса
session = requests.Session()

# Значение cookie
cookie_value = 'SL_G_WPT_TO=en; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; _gid=GA1.2.1042649071.1684313787; _ym_uid=1684313787290135952; _ym_d=1684313787; _ym_isad=1; intercom-device-id-ufjpx6k3=1b691db9-8635-4458-8134-4639ff5cf647; _grid_page_size=d3ebbdf9ec9235bfc4ba59572a6d3dd403a563222be148e9c705e91612194e49a:2:{i:0;s:15:"_grid_page_size";i:1;s:3:"200";}; _grid_page_size_schedule=35d0980fa38e2255112d0c62698773cab8aa12a81c6735caf172064b5eb6ea47a:2:{i:0;s:24:"_grid_page_size_schedule";i:1;s:3:"200";}; SERVERID=b430; userId=43161; createdTimestamp=1684324946; accessToken=e56ef9245b59cd46893ac373a024e161f3902121c246788a8c90eb2d90077e6a; SERVERID=b600; _backendMainSessionId=595d42692a18c7f469111a5662ee3064; _ym_visorc=w; _gat_gtag_UA_122842599_49=1; _ga_3QSGZBLTE3=GS1.1.1684324951.4.1.1684325806.0.0.0; _ga=GA1.1.1661591960.1684313787; intercom-session-ufjpx6k3=TlRzNnlBN2lhUXlyNklmSDFmZWFqNjdDcXl5cURCNW9IdzY1Q2JieEFnSVpKd2E0THI3TTd6V0ZMUy90MW5NdS0tSjA3T2NWSWpNZ09WTmFZamhDSGswUT09--a35dfe1bcca951353fad1c16f221ead7f1b67d60'

# Разделение значения cookie
cookie_list = cookie_value.split('; ')

# Установка каждого значения cookie
for cookie in cookie_list:
    cookie_name, cookie_value = cookie.split('=', 1)
    session.cookies.set(cookie_name, cookie_value)

# Выполнение запросов на сайт с использованием авторизационных cookie
response = session.get('https://backoffice.algoritmika.org/student?StudentSearch%5Bgroup_student_status%5D=0&StudentSearch%5Bcontent_type%5D%5B0%5D=course&StudentSearch%5Bcontent_type%5D%5B1%5D=intensive&StudentSearch%5BgroupType%5D%5B0%5D=masterclass&StudentSearch%5BgroupType%5D%5B1%5D=regular&StudentSearch%5BgroupType%5D%5B2%5D=intensive&StudentSearch%5BgroupType%5D%5B3%5D=individual&StudentSearch%5BisCourseInProgress%5D=1&presetType=active_v2&export=true&name=default&exportType=html')

# Проверка успешного выполнения запроса
if response.status_code == 200:
    # Обработка ответа
    print(response.text)
else:
    # Обработка ошибки
    print('Ошибка при выполнении запроса')
