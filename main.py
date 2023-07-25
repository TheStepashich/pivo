from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from pynput import keyboard
from pynput.keyboard import Key, Controller
import json
from threading import Thread
import pyaudio
import glob
import customtkinter
from PIL import Image as I
from customtkinter import filedialog
import requests
import wget
import webbrowser

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

INDEX = None
MAX_STR = 500
RANGE_WL = 'DataBase_auto!A2:B100'
RANGE_PS = 'PS!B6:E106'
LIGHT_IMAGE = 'light_radar.jpg'
DARK_IMAGE = 'dark_radar.jpg'

p = pyaudio.PyAudio()
for u in range(p.get_device_count()):
    # print(u, p.get_device_info_by_index(u)['name'])
    if 'CABLE Input (VB-Audio Virtual C' == p.get_device_info_by_index(u)['name']:
        INDEX = u
        break
    else: INDEX = 0

def read(file): # читает из json
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

INT_COLOR = '#966f02'
INT_COLOR_HOVER = '#735501'

def write(data, file): # сохраняет в json
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4,ensure_ascii=False)

def save_key(key, ptt, INDEX, path, user, tab_num, bus_model, bus_num, gov_num):# сохраняет в json
    class conf:
        def __init__(self) -> None:
            self.key = key
            self.ptt = ptt
            self.INDEX = INDEX
            self.path = path
            self.user = user
            self.tab_num = tab_num
            self.bus_model = bus_model
            self.bus_num = bus_num
            self.gov_num = gov_num
        
    data = {
        "conf": []
    }
    data['conf'].append(conf().__dict__)
    write(data, 'conf.json')


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

class no_reg(customtkinter.CTk):
    key = read('conf.json')['conf'][0]['key']
    ptt = read('conf.json')['conf'][0]['ptt']
    index = INDEX
    path = read('conf.json')['conf'][0]['path']
    user = read('conf.json')['conf'][0]['user']
    tn = read('conf.json')['conf'][0]['tab_num']
    b_number = read('conf.json')['conf'][0]['bus_num']
    model = read('conf.json')['conf'][0]['bus_model']
    g_number = read('conf.json')['conf'][0]['gov_num']
    tns = GoogleSheet().check_sheet(range=RANGE_WL)
    
    save_key(key, ptt, INDEX, path, user, tn,model, b_number, g_number)

    def __init__(self):
        super().__init__()
        self.geometry("400x350")
        self.resizable(width=False, height=False)
        self.title("ПИВО | Авторизация")
        self.iconbitmap('favicon.ico')
        self.focus_set()

        self.div_label = customtkinter.CTkFrame(master=self)
        self.div_label.pack(pady=0, padx=60, fill="both", expand=True)
        self.div_btns = customtkinter.CTkFrame(master=self)
        self.div_btns.pack(pady=0, padx=60, fill="both", expand=True)

        self.label_1 = customtkinter.CTkLabel(width=100, height=20, text= "Выберите ваше имя пользователя\nЕсли его нет - Напишите в поддержку. ", master=self.div_label, justify=customtkinter.LEFT)
        self.label_1.pack(pady=20, padx=20, expand = True, anchor ='n')

        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.div_btns, values=["Option 1", "Option 2", "Option 42 long long long..."])
        # self.optionmenu_1.pack(pady=0, padx=0, expand=False)
        # self.optionmenu_1.set("Выберите ваше имя")
        names = []
        for rows in self.tns:
            if rows[0]=='' or rows[0] == ' ':
                continue
            else:
                names.append(rows[0])
        print(names)
        self.list = customtkinter.CTkOptionMenu(master=self.div_btns,values=names, fg_color=INT_COLOR, button_color=INT_COLOR, button_hover_color=INT_COLOR_HOVER)
        self.list.pack(pady=0, padx=0, expand=False)
        # self.entry = customtkinter.CTkEntry(self.div_btns, placeholder_text="Введите никнейм")
        # self.entry.pack(pady=0, padx=0, expand=False)

        self.button_1 = customtkinter.CTkButton(text="Окей", fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, master=self.div_btns, command=self.button_callback)
        self.button_1.pack(pady=20, padx=0, expand=False)
    def button_callback(self):
        print("Button click", self.list.get())
        user_t = self.list.get()    
        
        for row in no_reg().tns:
            print(row[1], row[0])
            if row[0] == user_t and (user_t != '' and user_t != ' ' and user_t!='\n' and user_t != None):
                save_key(self.key, self.ptt, self.index, self.path, user_t, row[1], self.model, self.b_number, self.g_number)
                print(f'Сохранено имя пользователя {user_t}')
                self.list.configure(fg_color='green', button_color='green', button_hover_color='green', state='disabled')
                self.button_1.configure(state="disabled", fg_color='green', hover_color='green')
                main()
                self.destroy()
                break
            continue
        else:
                save_key(self.key, self.ptt, self.index, self.path, "", "", "", "", "")
    
class settings_win(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("340x300")
        self.focus_set()
        self.title("ПИВО | Настройки")
        self.iconbitmap('favicon.ico')
        self.resizable(width=False, height=False)
        # self.sett_frame = customtkinter.CTkFrame(master=self)
        # self.sett_frame.grid(row = 0, column = 0, columnspan = 2, rowspan = 3, sticky="nsew")
        # self.sett_frame.grid_columnconfigure(2, weight=0)
        # self.sett_frame.grid_rowconfigure(3, weight=0)
        
        self.label = customtkinter.CTkLabel(self, text="Настройки", font=customtkinter.CTkFont(size=20,weight='bold'))
        self.label.grid(row = 0, column = 0, padx=20, pady=20, columnspan = 2, sticky="n")

        self.sett_key = customtkinter.CTkLabel(master=self, text="Изменить клавишу \nинформатора")
        self.sett_key.grid(row=1, column=0, padx = 20, pady = 30, sticky="nw")

        self.sett_ptt = customtkinter.CTkLabel(master=self, text="Изменить клавишу \nбинд микрофона")
        self.sett_ptt.grid(row=2, column=0, padx = 20, pady = 30)

        self.sett_bus = customtkinter.CTkLabel(master=self, text="Изменить Автобус")
        self.sett_bus.grid(row=3, column=0, padx = 10, pady = 10)

        key = read('conf.json')['conf'][0]['key']
        ptt = read('conf.json')['conf'][0]['ptt']
        self.set_key = customtkinter.CTkButton(master=self,state= "normal", fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text=f"{key}", command=self.change_key_t)
        self.set_key.grid(row=1, column=1, padx = 20, pady = 30)

        self.set_ptt = customtkinter.CTkButton(master=self,state= "normal", fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text=f"{ptt}", command=self.change_ptt_t)
        self.set_ptt.grid(row=2, column=1, padx = 20, pady = 30)

        self.set_bus = customtkinter.CTkButton(master=self,state= "normal", fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text="Изменить автобус", command=self.change_bus)
        self.set_bus.grid(row=3, column=1, padx = 20, pady = 10)
        self.bus_window = None
    
    def change_bus(self):
        if self.bus_window is None or not self.bus_window.winfo_exists():
            self.bus_window = BusWindow(self)  # create window if its None or destroyed
        else:
            self.bus_window.focus()  # if window exists focus it

    def change_key_t(self):
        t = Thread(target=self.change_key)
        t.start()

    def change_key(self):
        self.set_key.configure(state="disable", hover = False)
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        listener.join()

    def change_ptt_t(self):
        t = Thread(target=self.change_ptt)
        t.start()

    def change_ptt(self):
        self.set_key.configure(state="disable", hover = False)
        listener = keyboard.Listener(on_press=self.on_press2)
        listener.start()
        listener.join()

    def on_press(self, key):
        
        try:
            tmp = key.char
            if '_l' in tmp: tmp = tmp.replace('_l', '')
            save_key(tmp, no_reg().ptt, no_reg().index, no_reg().path, no_reg().user, no_reg().tn, no_reg().model, no_reg().b_number, no_reg().g_number)
            self.set_key.configure(text=f"{tmp}", state = "normal", hover = True)
            if tmp: return False
        except AttributeError:
            tmp = str(key).replace('Key.', '')
            if '_l' in tmp: tmp = tmp.replace('_l', '')
            save_key(tmp,no_reg().ptt, no_reg().index, no_reg().path, no_reg().user, no_reg().tn, no_reg().model, no_reg().b_number, no_reg().g_number)
            self.set_key.configure(text=f"{tmp}",  state = "normal",  hover = True)
            if tmp: return False

    def on_press2(self, key):
        
        try:
            tmp = key.char
            if '_l' in tmp: tmp = tmp.replace('_l', '')
            save_key(no_reg().key, tmp, no_reg().index, no_reg().path, no_reg().user, no_reg().tn, no_reg().model, no_reg().b_number, no_reg().g_number)
            self.set_ptt.configure(text=f"{tmp}", state = "normal", hover = True)
            if tmp: return False
        except AttributeError:
            tmp = str(key).replace('Key.', '')
            if '_l' in tmp: tmp = tmp.replace('_l', '')
            save_key(no_reg().key,tmp, no_reg().index, no_reg().path, no_reg().user, no_reg().tn, no_reg().model, no_reg().b_number, no_reg().g_number)
            self.set_ptt.configure(text=f"{tmp}",  state = "normal",  hover = True)
            if tmp: return False

class BusWindow(customtkinter.CTkToplevel):
    key = read('conf.json')['conf'][0]['key']
    ptt = read('conf.json')['conf'][0]['ptt']
    index = read('conf.json')['conf'][0]['INDEX']
    path = read('conf.json')['conf'][0]['path']
    user = read('conf.json')['conf'][0]['user']
    tn = read('conf.json')['conf'][0]['tab_num']
    b_number = read('conf.json')['conf'][0]['bus_num']
    model = read('conf.json')['conf'][0]['bus_model']
    g_number = read('conf.json')['conf'][0]['gov_num']


    bus_table = GoogleSheet().check_sheet(range=RANGE_PS)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x300")
        self.resizable(width=False, height=False)
        self.title("ПИВО | Выбор автобуса")
        self.iconbitmap('favicon.ico')

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Выберите автобус из списка", width=480)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", columnspan = 2)
        self.scrollable_frame.grid_columnconfigure((0,1), weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.radio_var = customtkinter.IntVar(value=0)

        user = read('conf.json')['conf'][0]['user'] 
        
        i=0
        for row in self.bus_table:
            if row[3] in user:
                i+=1
                # Print columns A and E, which correspond to indices 0 and 4.
                self.radio_button = customtkinter.CTkRadioButton(master=self.scrollable_frame, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, variable=self.radio_var, value=row[0], text=f"{row[0] + ', ' + row[1] + ', ' + row[2] + ', ' + row[3]}")
                self.radio_button.grid(row=i, column=0, pady=5, padx=10, sticky="nw")
        self.bus_more_l = customtkinter.CTkButton(master=self, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text='Показать больше', command=self.bus_more)
        self.bus_more_l.grid(row=1, column = 1)
        self.bus_confirm = customtkinter.CTkButton(master=self, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text="Выбрать!", command=self.bus_confirms)
        self.bus_confirm.grid(row=1, column = 0)
    
    def bus_more(self):
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Выберите автобус из списка", width=480)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.radio_var = customtkinter.IntVar(value=0)
        
        i=0
        for row in self.bus_table:
            i+=1
            self.radio_button = customtkinter.CTkRadioButton(master=self.scrollable_frame, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, variable=self.radio_var, value=row[0], text=f"{row[0] + ', ' + row[1] + ', ' + row[2] + ', ' + row[3]}")
            self.radio_button.grid(row=i, column=0, pady=5, padx=10, sticky="nw")

    def bus_confirms(self):
        for row in self.bus_table:
            # print(row)
            if str(row[0]) == str(self.radio_var.get()):
                print(1)
                save_key(self.key,self.ptt,self.index,self.path,self.user,self.tn, str(row[1]), row[0], row[2])
                break
        self.destroy()
        

class already_reg(customtkinter.CTk):
    key = read('conf.json')['conf'][0]['key']
    ptt = read('conf.json')['conf'][0]['ptt']
    index = read('conf.json')['conf'][0]['INDEX']
    path = read('conf.json')['conf'][0]['path']
    user = read('conf.json')['conf'][0]['user']
    tn = read('conf.json')['conf'][0]['tab_num']
    b_number = read('conf.json')['conf'][0]['bus_num']
    model = read('conf.json')['conf'][0]['bus_model']
    g_number = read('conf.json')['conf'][0]['gov_num']
    tns = GoogleSheet().check_sheet(range=RANGE_WL)

    save_key(key, ptt, INDEX, path, user, tn,model, b_number, g_number)
    
    def __init__(self):
        super().__init__()

        # configure window
        self.geometry(f"{750}x{580}")
        self.resizable(width=False, height=False)
        self.title("ПИВО")
        self.put_el()

    def put_el(self):
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        if customtkinter.get_appearance_mode() == "Dark":
            self.test = customtkinter.CTkButton(self.sidebar_frame, text="ПИВО", hover_color="#2B2B2B", fg_color='#2B2B2B',text_color='white', font=customtkinter.CTkFont(size=20, weight="bold"), command=self.put_el)
        else:
            self.test = customtkinter.CTkButton(self.sidebar_frame, text="ПИВО", fg_color='#DBDBDB', hover_color='#DBDBDB', text_color="black",  font=customtkinter.CTkFont(size=20, weight="bold"), command=self.put_el)
        self.test.grid(row=0, column=0, padx=20, pady=(20, 10))
        # self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="ПИВО", font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        
        
        self.radio_var = customtkinter.IntVar(value=0)
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.sidebar_frame, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, variable=self.radio_var, value=0, text="Текстовый информатор")
        self.radio_button_1.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.sidebar_frame, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, variable=self.radio_var, value=1, text="Голосовой информатор")
        self.radio_button_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.button_3 = customtkinter.CTkButton(master=self.sidebar_frame, text="Настройки", fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, command=self.settings)
        self.settings_win = None
        self.button_3.grid(row=3, column=0, pady=10, padx=20, sticky="n")

        self.music = customtkinter.CTkButton(master=self.sidebar_frame, text="Включить музыку", fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, command=self.music)
        self.music.grid(row=4, column=0, pady=10, padx=20, sticky="n")

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Тема оформления:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, button_color=INT_COLOR, fg_color=INT_COLOR, button_hover_color=INT_COLOR_HOVER, values=["Dark","System", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Масштабирование UI:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,button_color=INT_COLOR, fg_color=INT_COLOR,button_hover_color=INT_COLOR_HOVER, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.mainframe = customtkinter.CTkFrame(master=self)
        self.mainframe.grid(row=0, column=1, rowspan=4, columnspan = 1, sticky="nsew", padx = 0)
        self.mainframe.grid_rowconfigure(4, weight=1)
        # self.mainframe.grid_columnconfigure(1, weight=0)
        
        self.hello = customtkinter.CTkLabel(self.mainframe, text=f"Добро пожаловать, {self.user} !", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.hello.grid(row=0, column=0,columnspan = 2, padx=20, pady=(20, 10))

        self.bus = customtkinter.CTkLabel(self.mainframe, text=f"Автобус - {read('conf.json')['conf'][0]['bus_model']}", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bus.grid(row=1, column=0,columnspan = 2, padx=20, pady=(20, 10))

        self.your_image = customtkinter.CTkImage(light_image=I.open(os.path.join(LIGHT_IMAGE)), dark_image=I.open(os.path.join(DARK_IMAGE)), size=(350 , 350))
        self.label123 = customtkinter.CTkLabel(master=self.mainframe, image=self.your_image, text='')
        self.label123.grid(row=4, column=0, columnspan = 2)
        
        self.btn_frame = customtkinter.CTkFrame(master=self.mainframe)
        self.btn_frame.grid(row=5, column=0, columnspan = 2, padx = 20, pady = 20)
        
        self.startgame = customtkinter.CTkButton(self.btn_frame, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text="Запустить игру!", command=self.start_game)
        self.startgame.grid(row=0, column = 0, padx=10, pady = 5)
        self.startinf = customtkinter.CTkButton(self.btn_frame, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text="Запустить Информатор", command=self.start_inf)
        self.startinf.grid(row=0, column = 1, padx=10, pady = 5)

    def start_game(self):
        if read('conf.json')['conf'][0]['path'] == '':
            filename = filedialog.askopenfilename(title="Выберите Multi Theft Auto.exe", initialdir="C:/Games/MTA Province/MTA")
            # save_key(read('conf.json')['conf'][0]['key'],read('conf.json')['conf'][0]['INDEX'],filename)
            save_key(self.key, self.ptt, self.index, filename, self.user, self.tn, self.model, self.b_number, self.g_number)
            os.startfile(filename)
        else:
            filename = read('conf.json')['conf'][0]['path']
            os.startfile(filename)
            print('from saved')

    def start_inf(self):
        routes = []
        for files in glob.glob("routes\\*"):
            routes.append(files.replace('routes\\','').replace('\\',''))
        print(routes)
        self.startinf.destroy()
        self.startgame.destroy()
        self.startinf = customtkinter.CTkOptionMenu(master=self.btn_frame , fg_color=INT_COLOR, button_color=INT_COLOR, button_hover_color=INT_COLOR_HOVER, values=routes)
        self.startinf.grid(row=0, column = 1, padx=10, pady = 5)
        self.startinf2 = customtkinter.CTkButton(master=self.btn_frame, text=" > ", fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, command=self.start_inf_t)
        self.startinf2.grid(row = 0, column = 2, padx = 5, pady = 5)
    
    def stop_inf(self):
        with keyboard.Controller().pressed(Key.ctrl):
            keyboard.Controller().press('x')
            keyboard.Controller().release('x')
        keyboard.Controller().release(Key.ctrl)
    
    def start_inf_t(self):
        t = Thread(target=self.start_inf2)
        t.start()
    def start_inf2(self):
        with open('tmp.txt', 'w', encoding='utf-8') as f:
            f.write('date\n')
            f.write(self.startinf.get())
            
        if self.radio_var.get() == 0:
            print('text')
            self.startinf2.destroy()
            self.startinf.destroy()
            self.stopinf = customtkinter.CTkButton(master=self.btn_frame, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text="Остановить информатор", command=self.stop_inf)
            self.stopinf.grid(row=0, column = 0, columnspan = 2)  
            import informator
        
        if self.radio_var.get() == 1:
            print('voice')
            self.startinf2.destroy()
            self.startinf.destroy()
            self.stopinf = customtkinter.CTkButton(master=self.btn_frame, fg_color=INT_COLOR, hover_color=INT_COLOR_HOVER, text="Остановить информатор", command=self.stop_inf)
            self.stopinf.grid(row=0, column = 0, columnspan = 2)
            import voice
  

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if customtkinter.get_appearance_mode() == "Dark":
            self.test.configure(hover_color="#2B2B2B", fg_color='#2B2B2B', text_color = 'white')
        elif customtkinter.get_appearance_mode() == "Light":
            self.test.configure(fg_color='#DBDBDB', hover_color='#DBDBDB', text_color = 'black')
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def settings(self):
        if self.settings_win == None or not self.settings_win.winfo_exists():
            self.settings_win = settings_win(self)
            self.settings_win.focus
              # create window if its None or destroyed
        else:
            self.settings_win.focus()  # if window exists focus it
    
    def music(self):
        webbrowser.open('https://volnorez.com/molot')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{200}x{100}")
        self.resizable(width=False, height=False)
        self.title("ПИВО | Обновления")
        self.show_warning()
    def show_warning(self):
        self.label = customtkinter.CTkLabel(master=self, text='Программа обновляется.')
        self.label.pack()

def download_upd():
    app = App()
    install_file = 'PIVO_INSTALL.exe'
    if os.path.isfile(install_file):
        os.remove(install_file)
        wget.download(url='https://github.com/TheStepashich/pivo/releases/download/kareta/PIVO_INSTALL.exe', out='PIVO_INSTALL.exe')
    else: 
        wget.download(url='https://github.com/TheStepashich/pivo/releases/download/kareta/PIVO_INSTALL.exe', out='PIVO_INSTALL.exe')
    os.startfile('PIVO_INSTALL.exe')
    os.abort()

def main():
    try:
        response = requests.get(url='https://raw.githubusercontent.com/TheStepashich/pivo/main/ver.txt')
        if response.text.removesuffix('\n') == 'v1.1.4':
            print(response.text)
        else:
            print('Программа устарела', response.text)
            download_upd()
    except Exception as _ex:
        print('err')


    user = read('conf.json')['conf'][0]['user']
    if user == '' or user == ' ':
        app = no_reg()
    elif user != '' and user != ' ' and user !='\n':
        app = already_reg()
        app.iconbitmap('favicon.ico')
    app.mainloop()

if __name__ == "__main__":
    main()
