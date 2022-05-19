import numpy as np
from random import uniform
from time import sleep
import pyautogui as pag
import cv2 as opencv
import pydirectinput as pdi
import pynput
from win32gui import GetWindowText, GetForegroundWindow
'''
Health globe of PoE at around 30% life is y coordinate ~1000
spanning across horizontally from 110 to 125
'''
YPOS = 1000
X_RANGE = (70, 170)
ROWS_OF_PIXELS = 5
full_life_mean = np.array([118.164, 13.866, 21.914])
delta = 48.1
is_low_life = False
active_window_preferred = 'Path of Exile'
# 328 1058, 16, 16, 17 (flask empty)
flask_empty_pos = (328, 1058)
flask_empty_color = [16,16,17]

def checkCurrentWindow() -> bool:
    active = GetForegroundWindow()
    title = GetWindowText(active)
    return title in active_window_preferred

def checkFlaskEmpty() -> bool:
    grab = pag.screenshot(region=(*flask_empty_pos,1,1))
    img = np.array(grab)[0][0]
    return all([img[i] == flask_empty_color[i] for i in range(3)])

def checkIfLowLife():
    global is_low_life
    while 1:
        # pag.displayMousePosition();
        if not checkCurrentWindow():
            print('\rPoE not active window...', end = '                     ', flush=True); continue
        print('\rIs Low Life? : ', 'Yes' if is_low_life else 'No ', flush=True, end = '')
        print(f'   | Flask Empty : ', 'Yes' if checkFlaskEmpty() else 'No', flush=True, end='   ')
        grab = pag.screenshot(region=
            (
                X_RANGE[0], 
                YPOS,
                X_RANGE[-1] - X_RANGE[0],
                ROWS_OF_PIXELS
            )
        )
        img = np.array(grab)
        mean = np.average(img[0], axis=0)
        if any(res :=[abs(mean[i]-full_life_mean[i]) > delta for i in range(3)]):
            is_low_life = True
            pag.press('1')
            sleep(.06 + uniform(-.02123, .011738)) # dont spam flask
            # [print(abs(mean[i]-full_life_mean[i])) for (i, x) in enumerate(res) if x]
            # print('Delta hit!~', flush=True)
        else: is_low_life = False

def main():
    print('Started checking life', flush=True)    
    checkIfLowLife()
    print('Stopped checking life')    
if __name__ == '__main__':
    main()
