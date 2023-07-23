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
import customtkinter
customtkinter.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"




class no_reg(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.geometry("400x350")
        self.title("CustomTkinter simple_example.py")
        self.focus_set()

        self.div_label = customtkinter.CTkFrame(master=self)
        self.div_label.pack(pady=0, padx=60, fill="both", expand=True)
        self.div_btns = customtkinter.CTkFrame(master=self)
        self.div_btns.pack(pady=0, padx=60, fill="both", expand=True)

        self.label_1 = customtkinter.CTkLabel(width=100, height=20, text= "Выберите ваше имя пользователя", master=self.div_label, justify=customtkinter.LEFT)
        self.label_1.pack(pady=20, padx=20, expand = True)

        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.div_btns, values=["Option 1", "Option 2", "Option 42 long long long..."])
        # self.optionmenu_1.pack(pady=0, padx=0, expand=False)
        # self.optionmenu_1.set("Выберите ваше имя")

        self.entry = customtkinter.CTkEntry(self.div_btns, placeholder_text="Введите никнейм")
        self.entry.pack(pady=0, padx=0, expand=False)

        self.button_1 = customtkinter.CTkButton(text="Окей", master=self.div_btns, command=self.button_callback())
        self.button_1.pack(pady=20, padx=0, expand=False)
    
    def button_callback(self):
        print("Button click", self.entry.get())
        user_t = self.entry.get()
        for row in no_reg().tns:
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
    
class already_reg(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="ПИВО", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.mainframe = customtkinter.CTkFrame(master=self)
        self.mainframe.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.hello = customtkinter.CTkLabel(master=self.mainframe, text=f'Добро пожаловать!', font=customtkinter.CTkFont(family="Arial", size=20))
        self.hello.grid(row=0, column = 0, pady = 20, padx = 20)



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)





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
    if user == ' ' or user == '':
        app = no_reg()
            # user_t = input(no_reg().button_callback())
            
            
            
            # user_t = input('Введите ваше имя пользователя: ')
            
        # elif user != ' ':
        #     for row in tns:
        #         tn+=1
        #         print(tn, row[0], user)
        #         if row[0] == user.removesuffix('\n'):
        #             print(f'Вы вошли как {user}')
        #             file.seek(0)
        #             file.write(user)
        #             file.write(str(tn))
        #             print(str(tn))
        #             break
        #         continue
            
        #     else:
        #         print('Ошибка входа! Возможно ваше имя пользователя заблокировано или удалено из списка!')
        #         file.seek(0)
        #         file.write(' ')
        #         os.abort()
                    
    
    app.mainloop()
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
    # n = int(input())
    # if n == 1:
    app = already_reg()
    # if n == 0:
    #     app = no_reg()
