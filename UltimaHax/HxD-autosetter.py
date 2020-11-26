import os
import time
from pynput.keyboard import Key, Listener, Controller


# XXXXX: (fix ASAP!)
# KEIRA: (main headers)
# kkkkk: (sub-headers)
# KKKKK: (sub sub-headers)

# TODO: (incomplete)
# QUESTION: (wt* did i just do)


# KEIRA: (Offsets) **************

# kkkkk: (CHAR STATS)
# Strength:     (0x000E)
# Intelligence: (0x000F)
# Dexterity:    (0x0010)
# Magic:        (0x0011)
# HP:           (0x0012) (0x0013)
# HM:           (0x0014) (0x0015)
# Experience:   (0x0016) (0x0017)
# Gold:         (0x0204) (0x0205)


# keira: (OS methods) --------------------------------------------------------------------------------------------------
def openFile():
    try:
        os.startfile('../SAVED.GAM')
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


def enter(key):
    keyboard = Controller()
    keyboard.press(key)
    keyboard.release(key)


# keira: (SAVED.GAM methods) -------------------------------------------------------------------------------------------
# kkkkk: Given a hex value (bigEnd), overwrites char stats based on its length (2 or 4)
# KKKKK: (NOTE: this does not account for hex values w/ length > 4!)
def editCharStats():
    for i in range(4):
        enter('6')
        enter('3')
    for i in range(3):
        enter('e')
        enter('7')
        enter('0')
        enter('3')
    for i in range(6):
        enter(Key.right)
    enter(Key.down)

def editALLCharStats():
    # KKKKK: (14 spaces @ start of file)
    for i in range(14):
        enter(Key.right)
    # KKKKK: (15 characters)
    for i in range(16):
        editCharStats()

def saveFile():
    enter(Key.alt_l)
    enter('f')
    for i in range(5):
        enter(Key.down)
    enter(Key.enter)


# keira: (CONVERSION methods) -----------------------------------------------------------------------------------------
def hexOf(dec):
    hexValue = "{0:x}".format(dec)
    if (len(hexValue) % 2 != 0):
        newHexValue = "0"
        newHexValue += hexValue
        return newHexValue
    return hexValue

def littleEndianOf(bigEndian):
    return "".join(reversed([bigEndian[i:i+2] for i in range(0, len(bigEndian), 2)]))

# keira: (MAIN methods) ------------------------------------------------------------------------------------------------
def editSavedGAM():
    openFile()
    time.sleep(0.5)
    print("done")
    editALLCharStats()
    time.sleep(0.5)
    saveFile()
    ##closeFile()


# keira: (MAIN) ********************************************************************************************************

# hexVal = hexOf(999)
# print(hexVal)
# print(type(hexVal))
# print(littleEndianOf(hexVal))
editSavedGAM()


# keira: (LISTENER) ----------------------------------------------------------------------------------------------------
# with Listener(on_press=on_press,
#               on_release=on_release) as listen:
#     listen.join()
