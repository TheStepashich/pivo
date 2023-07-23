from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from pynput import keyboard
import json
import pyaudio

INDEX = None
MAX_STR = 500
RANGE_WL = 'DataBase_auto!A2:B100'

class GoogleSheet:
    SPREADSHEET_ID = '1GGf2GYGYyVDG37FGyE43fCviecS2DNj6PR6L279cE2o'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)
    
    def check_sheet(self, range):
        values = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                        range=range,
        
                                                        majorDimension='ROWS').execute()
        return values.get('values', [])

def read(file): # читает из json
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

n_data = read('conf.json')
key = n_data['conf'][0]['key']
ptt = n_data['conf'][0]['ptt']

def on_press(key): # в tmp имя нажатой клавиши
        try:
            tmp = key.char
            if '_l' in tmp: tmp = tmp.replace('_l', '')
            keyboard.Listener.stop
            save_key(tmp)
        except AttributeError:
            tmp = str(key).replace('Key.', '')
            if '_l' in tmp: tmp = tmp.replace('_l', '')
            keyboard.Listener.stop
            save_key(tmp, INDEX)

def write(data, file): # сохраняет в json
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def save_key(key, INDEX):# сохраняет в json
    
    class conf:
        def __init__(self) -> None:
            self.key = key
            self.ptt = ptt
            self.INDEX = INDEX
        

    data = {
        "conf": []
    }

    data['conf'].append(conf().__dict__)
    write(data, 'conf.json')

p = pyaudio.PyAudio()
for u in range(p.get_device_count()):
    # print(u, p.get_device_info_by_index(u))
    if 'CABLE Input (VB-Audio Virtual C' == p.get_device_info_by_index(u)['name']:
        INDEX = u
save_key(key, INDEX)


def main(): # TODO
    with open("user.conf", 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        user = ''.join(lines[0:1])
        tn = 0
        b_number = ''.join(lines[2:3])
        model = ''.join(lines[3:4])
        if model == '': model = 'Выберите Автобус в настройках!'
        g_number = ''.join(lines[4:5])
        tns = GoogleSheet().check_sheet(range=RANGE_WL)
        if user == ' ' or user == '':
            user_t = input('Введите ваше имя пользователя: ')
            for row in tns:
                tn+=1
                # print(tn, row[0])
                if row[0] == user_t:
                    file.seek(0)
                    file.write(user_t+'\n')
                    file.write(str(tn))
                    user = user_t
                    print(f'Сохранено имя пользователя {user_t}')
                    break
                continue
            else:
                    print('Ошибка входа! Неверный Никнейм. Обратитесь в поддержку!')
                    tn = 0
                    file.seek(0)
                    file.write(' ')
                    os.abort()
        elif user != ' ':
            for row in tns:
                tn+=1
                print(tn, row[0], user)
                if row[0] == user.removesuffix('\n'):
                    print(f'Вы вошли как {user}')
                    file.seek(0)
                    file.write(user)
                    file.write(str(tn))
                    print(str(tn))
                    break
                continue
            
            else:
                print('Ошибка входа! Возможно ваше имя пользователя заблокировано или удалено из списка!')
                file.seek(0)
                file.write(' ')
                os.abort()
                    
    file.close()
    
    true = True
    while true:
        print(f"Информатор ООО Карета. Для выбора пункта меню, напишите цифру соответствующего пункта и нажмите Enter! \n--- Главное меню --- \n Ваше имя пользователя: {user.removesuffix('n')+' '}Автобус: {g_number+' '+model}")
        n = int(input("[1] - Запустить текстовый информатор. \n[2] - Запустить голосовой информатор. \n[3] - Настройки. \n[0] - Выход. \n"))

        if n == 0: os.abort()
        elif n == 1:
            true = False
            import informator
        
        elif n == 2:
            true = False
            import voice
        elif n == 3:
            true = False
            true_s = True
            while true_s:
                print("Информатор ООО Карета. Для выбора пункта меню, напишите цифру соответствующего пункта и нажмите Enter! \n--- Раздел настройки --- \n")
                n = int(input(f"[1] - Изменить клавишу информатора ({n_data['conf'][0]['key']}). \n[2] - Изменить автобус {g_number+' '+model}\n[0] - Назад. \n"))
                if n == 0:
                    true = True
                    break
                    
                elif n == 1:
                    print("Введите новую клавишу информатора. ")
                    with keyboard.Listener(
                        on_press=on_press) as listener:
                            listener.join()
                    keyboard.Listener.stop(self=listener)
                    true = False
                    os.abort()
                elif n == 2:
                    true = False
                    print('Введите бортовой номер машины из списка:')
                    username = open('user.conf', 'r').readline()
                    gs = GoogleSheet()
                    print(' №       Модель           Гос. номер      Водитель')
                    
                    data = gs.check_sheet('PS!B6:E50')
                    for row2 in data:
                        if row2[3] in username:
                            # Print columns A and E, which correspond to indices 0 and 4.
                            print('%s | %s | %s | %s' % (row2[0], row2[1], row2[2], row2[3]))
                    bn = input()

                    for row2 in data:
                        if row2[0] == bn:
                            with open('user.conf', 'w', encoding='utf-8') as f:
                                f.write(username)
                                f.write(str(tn)+'\n')
                                f.write(bn+'\n')
                                f.write(row2[1]+'\n')
                                model = row2[1]
                                f.write(row2[2])
                                g_number = row2[2]


if __name__ == '__main__':
    main()