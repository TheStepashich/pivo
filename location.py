import pyautogui
import time
import settings
import monitoring
color = (131, 197, 226)
def run():
    chatp = open('tmp.txt').readline()
    m = open('tmp.txt').readline()
    while True:
        if not settings.located_status:
            print('Finished!')
            break
        img = pyautogui.screenshot()
        print('SCREEN')
        (width, height) = img.size
        f = False
        for x in range(0, width, 1):
            for y in range(0, height, 1):
                if color == img.getpixel((x, y)):
                    
                    x = str((x -   (width - height)//2)*1500//height)
                    y = str(y * 1450 // height - 40)
                    print(x,y)
                    with open('tmp.txt', 'w') as file:
                        file.write(m+'\n')
                        file.write(x+'\n')
                        file.write(y)

                    #print(x*1500/width)
                    f = True
                    break
                    # return (x/width*1000, y/height*1000)
            if f:
                break
        monitoring.main()
        time.sleep(5)

