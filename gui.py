from tkinter import *
import time
import keyboard
import os
from PIL import ImageTk, Image


window = Tk()
#размеры окна
window.geometry("60x55-60-80")

#Выше всех
window.overrideredirect(1)
window.bind("<Escape>", lambda event: window.destroy())

def window_open(event):
    window.geometry("500x400-60-80")
def window_close(event):
    window.geometry("60x55-60-80")

img = ImageTk.PhotoImage(Image.open("icon.ico"))
l = Label(image=img)
l.pack()



def windshow():
    global windshowed
    
    if windshowed == False:
        time.sleep(0.40)

        window.deiconify()

        window.attributes('-topmost',True)
        window.grab_release()
        windshowed = True
    else:
        window.withdraw()
        windshowed = False
    
windshowed = False     

window.bind('<Button-1>', window_open)
window.bind('<Leave>', window_close)

keyboard.add_hotkey('u', windshow, suppress=False)
window.withdraw()



window.mainloop()