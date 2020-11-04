
import os
import time
from pynput.keyboard import Key, Listener, Controller

# XXXXX: (fix ASAP!)
# KEIRA: (main headers)
# KKKKK: (sub-headers)
# kkkkk: (sub sub-headers)
# TODO: (incomplete)
# QUESTION: (wtf did i just do)

# keira: (OS methods) --------------------------------------------------------------------------------------------------
def openFile():
    try:
        os.startfile('SAVED.GAM')
    except Exception as e:
        print(str(e))

def closeFile():
    try:
        os.system('TASKKILL /F /IM HxD.exe')

    except Exception as e:
        print(str(e))

# keira: (CONTROLLER methods) ------------------------------------------------------------------------------------------
def on_press(key):
    print(f"{key}")

def on_release(key):
    if key == Key.esc:
        return False

def type(key):
    keyboard = Controller()
    keyboard.press(key)
    keyboard.release(key)

# keira: (SAVED.GAM methods) -------------------------------------------------------------------------------------------
def editCharStats():
    for i in range(4):
        type('6')
        type('3')
    for i in range(3):
        type('e')
        type('7')
        type('0')
        type('3')
    for i in range(6):
        type(Key.right)
    type(Key.down)

def editALLCharStats():
    # KKKKK: (14 spaces @ start of file)
    for i in range(14):
        type(Key.right)
    # KKKKK: (15 characters)
    for i in range(16):
        editCharStats()

def saveFile():
    type(Key.alt_l)
    type('f')
    for i in range(5):
        type(Key.down)
    type(Key.enter)

openFile()
time.sleep(0.5)
print("done")
editALLCharStats()
time.sleep(0.5)
saveFile()
closeFile()

# keira: (LISTENER) ----------------------------------------------------------------------------------------------------
# with Listener(on_press=on_press,
#               on_release=on_release) as listen:
#     listen.join()
