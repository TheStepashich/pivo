import time as t
import keyboard as k
import os
import json
import datetime

def close():
    with open('tmp.txt', 'w') as tmp_txt:
        tmp_txt.write(' ')
        tmp_txt.write(' ')
        tmp_txt.write(' ')
        os.startfile('monitoring.exe')
        os.abort()

def send_data(route, line, date):
    lline = str(line).replace('/do ', '')

    with open('tmp.txt', 'w') as tmp_txt:
        tmp_txt.write(str(date)+str('\n'))
        tmp_txt.write(str(route+'\n'))
        tmp_txt.write(lline)
        os.startfile('monitoring.exe')
        return

def txt_inf():
    line = f.readline()
    if line == '':
        os.abort()
    
    k.send('t')
    t.sleep(0.1)
    k.write(line)
    t.sleep(0.1)
    k.send('Enter')
    print(line)
    
    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')
    now = datetime.datetime.now(tz=tz)
    send_data(route, line, now.strftime("%d-%m-%Y %H:%M:%S"))
    t.sleep(5)


def read(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


key = read('conf.json')['conf'][0]['key']

# routes = []
# for files in glob.glob("routes\\*"):
#     routes.append(files)
# m_number = str(routes).replace('routes\\','').replace('\\','')
# print(f' Доступные маршруты: \n','   1     2     3     4   \n', (str(m_number))) # тут нужно красиво сделать
# n = int(input('Вводим нужный маршрут по счету \n'))-1
with open('tmp.txt', 'r') as tmpf:
    lines = tmpf.readlines()
    route = ''.join(lines[1:2])

# filename = str(routes[n])+(str(routes[n]).replace('routes', ''))+('.txt')
filename = f'routes\\{route}\\{route}.txt'
# m_number = str(routes[n]).replace('routes\\', '')
f = open(filename,'r' )

print(f"Информатор по маршруту №{route}. Для проигрывания сообщений информатора нажмите кнопку {key}. \n")

k.add_hotkey(key, txt_inf)
k.add_hotkey('ctrl+x', close)
k.wait()