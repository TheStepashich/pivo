import json
import wave
import os
import glob
import pyaudio
import keyboard
import datetime


CHUNK = 1024

def close():
    with open('tmp.txt', 'w') as tmp_txt:
        tmp_txt.write(' ')
        tmp_txt.write(' ')
        tmp_txt.write(' ')
        os.startfile('monitoring.exe')
        os.abort()

def write(data, file):
    data = json.dumps(data)
    data = json.loads(str(data))
    with open('conf.json', 'w') as f:
        json.dump(data, f, indent=4)

def read(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

offset = datetime.timedelta(hours=3)
tz = datetime.timezone(offset, name='МСК')
now = datetime.datetime.now(tz=tz)
n_data = read('conf.json')
key = n_data['conf'][0]['key']
ptt = n_data['conf'][0]['ptt']
vlist = []

global i
i = -1
index = n_data['conf'][0]['INDEX']

def send_data(m_number, line, date):
    lline = str(line).replace(f'routes\\{m_number}\\', '')
    
    if len(str(m_number)) == 1:
        print(1)
        if lline[0] == str(m_number)[0] :
            with open(f"routes\\{m_number}\\{m_number}.txt", 'r') as tfile:
                location = tfile.readlines()
            location = ''.join(location[i:(i+1)]).replace('/do ', '')
    
    elif len(str(m_number)) == 2:
        print(2)
        print(lline[0]+lline[1])
        if lline[0] + lline[1] == str(m_number):
            with open(f"routes\\{m_number}\\{m_number}.txt", 'r') as tfile:
                location = tfile.readlines()
            location = ''.join(location[i:(i+1)]).replace('/do ', '')
    
    else:
        print(3)
        if lline[0] + lline[1] + lline[2] == str(m_number)[0] + str(m_number)[1] + lline[2]:
            with open(f"routes\\{m_number}\\{m_number}.txt", 'r') as tfile:
                location = tfile.readlines()
            location = ''.join(location[i:(i+1)]).replace('/do ', '')
    
    with open('tmp.txt', 'w') as tmp_txt:
        tmp_txt.write(str(date)+str('\n'))
        tmp_txt.write(str(m_number+'\n'))
        tmp_txt.write(location)
        print(location)
        os.startfile('monitoring.exe')
        return

def play():
    
    p = pyaudio.PyAudio()

    keyboard.press(ptt)
    global i
    i+=1
    if i == len(vlist): 
        os.abort()
    
    send_data(route, vlist[i], now.strftime("%d-%m-%Y %H:%M:%S"))
    with wave.open(vlist[i], 'rb') as wf:
        print(vlist[i])
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=index
                        )

        while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
            stream.write(data)

        stream.close()
        keyboard.release(ptt)

        # Release PortAudio system resources (5)
        p.terminate()

with open('tmp.txt', 'r') as tmpf:
    lines = tmpf.readlines()
    route = ''.join(lines[1:2]).removesuffix("\n")

for file in glob.glob(f"routes\\{route}\\{route}*.wav"):
    vlist.append(file)
print(vlist)
print(f"Информатор по маршруту №{route}. Для проигрывания сообщений информатора нажмите кнопку {key}. \n")


keyboard.add_hotkey(key, play)
keyboard.add_hotkey('ctrl+x', close)
keyboard.wait()