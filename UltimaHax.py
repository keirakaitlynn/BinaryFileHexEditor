

# XXXXX:     (fix ASAP!)          (#c6001a)
# KEIRA:     (main headers)       (#ff0070)
# kkkkk:     (sub-headers)        (#fcb9c5)
# KKKKK:     (sub sub-headers)    (#b97474)
# TODO:      (incomplete)         (#ccff00)
# QUESTION:  (wtf did i just do)  (#00b9ff)


# KEIRA: (OFFSETs) -----------------------------------------------------------------------------------------------------

chars_OFFSET = {
    "goldfish": 0x0000,
    "Shamino":  0x0020,
    "Iolo":     0x0040,
    "Mariah":   0x0060,
    "Geoffrey": 0x0080,
    "Jaana":    0x00A0,
    "Julia":    0x00C0,
    "Dupre":    0x00E0,
    "Katrina":  0x0100,
    "Sentri":   0x0120,
    "Gweno":    0x0140,
    "Johne":    0x0160,
    "Gorn":     0x0180,
    "Maxwell":  0x01A0,
    "Toshi":    0x01C0,
    "Saduj":    0x01E0
}

stats_OFFSET = {
    "strength":     [0x000E],
    "intelligence": [0x000F],
    "dexterity":    [0x0010],
    "magic":        [0x0011],
    "hp":           [0x0012, 0x0013],
    "max hp":       [0x0014, 0x0015],
    "experience":   [0x0016, 0x0017],
    "gold":         [0x0204, 0x0205]
}

items_OFFSET = {
    "keys":          [0x0000],
    "skull keys":    [0x0000],
    "gems":          [0x0000],
    "black badge":   [0x0000],
    "magic carpets": [0x0000],
    "magic axes":    [0x0000]
}

things_MAXVAL = {
    "strength":      99,
    "intelligence":  99,
    "dexterity":     99,
    "magic":        255,
    "hp":           999,
    "max hp":       999,
    "experience":  9999,
    "gold":        9999,  # QUESTION: 32767?
    "keys":          99,  # QUESTION: wants 100
    "skull keys":    99,  # QUESTION: wants 100
    "gems":          99,  # QUESTION: wants 100
    "black badge":    1,  # QUESTION: 00, FF?
    "magic carpets": 99,
    "magic axes":    99,
    "all":           99
}


# keira:  (SAVED.GAM methods) ------------------------------------------------------------------------------------------
# kkkkk: Given offset & numOfBytes to read,
#        moves pointer to the byte located at that offset,
#        reads this byte & the following numOfBytes,
#        & converts this array of bytes to dec.
def readByte(file, offset):
    return readBytes(file, offset, 1)

def readBytes(file, offset, numOfBytes):
    with open(file, 'rb') as file:
        file.seek(offset, 1)  # set curr. position of pointer to offset.
        # assert file.tell() == 0x000E
        byte_array = file.read(numOfBytes)
        return decOf(byte_array)

# kkkkk: Given offset & dec, moves pointer to the byte located at that offset & changes its value to hexOf(dec).
def setByte(file, offset, dec):
    byte_array = byteArrayOf(littleEndianOf(hexOf(dec)))

    # 'r+b': used to...
    #        - open & read file ('r')
    #        - read file as a binary file, so that the bytes of the file won't be encoded when read ('b')
    #        - overwrite data, rather than truncate the rest ('+')

    with open(file, 'r+b') as file:
        file.seek(offset)
        # assert file.tell() == 0x000E
        file.write(byte_array)

def setBytes(file, offset, dec):
    byte_array = byteArrayOf(littleEndianOf(hexOf(dec)))
    if len(byte_array) != 2:
        byte_array.append(0)

    with open(file, 'r+b') as file:
        file.seek(offset)
        # assert file.tell() == 0x000E
        file.write(byte_array)

# kkkkk: Given char, stat & dec, sets stat of char to dec.
def setStat(file, char, stat, dec):
    if len(stats_OFFSET[stat]) == 2:
        setBytes(file, chars_OFFSET[char] + stats_OFFSET[stat][0], dec)
    else:
        setByte(file, chars_OFFSET[char] + stats_OFFSET[stat][0], dec)

# kkkkk: Given dec, sets ALL stats of ALL chars to dec.
def setStat4ALLChars(file, stat, dec):
    for char in chars_OFFSET:
        setStat(file, char, stat, dec)

# kkkkk: Given char & dec, sets ALL stats of char to dec.
def setALLStats(file, char, dec):
    for stat in stats_OFFSET:
        setStat(file, char, stat, dec)

# kkkkk: Given dec, sets ALL stats of ALL chars to dec.
def setALLStats4ALLChars(file, dec):
    for char in chars_OFFSET:
        setALLStats(file, char, dec)


# keira:  (CONVERSION methods) -----------------------------------------------------------------------------------------
# kkkkk:  Given a DECIMAL value, returns its HEXADECIMAL value.
def hexOf(dec):
    hexValue = "{0:x}".format(dec)
    # KKKKK: If hexValue is ODD, add a 0 in front of it.
    if (len(hexValue) % 2 != 0):
        newHexValue = "0"
        newHexValue += hexValue
        return newHexValue
    return hexValue

# kkkkk:  Given a BIG-ENDIAN hexadecimal value, returns its LITTLE-ENDIAN hexadecimal value.
def littleEndianOf(bigEndian):
    return "".join(reversed([bigEndian[i:i+2] for i in range(0, len(bigEndian), 2)]))

# kkkkk:  Given a HEXADECIMAL value, returns its BYTE-ARRAY.
# KKKKK: (NOTE: when writing to SAVED.GAM, hexValue must be a LITTLE-ENDIAN hexadecimal value.)
def byteArrayOf(hexValue):
    return bytearray.fromhex(hexValue)

def decOf(byteArray):
    return int.from_bytes(byteArray, 'little')


# keira:  (MAIN methods) -----------------------------------------------------------------------------------------------
# kkkkk: Given thing_TYPE ("CHARACTER" / "STAT" / "ITEM") & its things_OFFSET, displays its menu.
def displayMenu(thing_TYPE, things_OFFSET):
    num = 1
    print("----- (" + thing_TYPE.upper() + "S) --------------")
    name = ""
    for thing in things_OFFSET:
        print("\t (" + str(num) + ") " + thing)
        num += 1
    print("\t (" + str(num) + ") ALL " + thing_TYPE.upper() + "S")
    print("---------------------------------")

def getOption(maxOptions):
    option = 0
    while option not in range(1, maxOptions+1):
        option = int(input("Select an option "
                           "(1-" + str(maxOptions) + "): "))
    return option

def getChar():
    displayMenu("CHARACTER", chars_OFFSET)
    return validate("CHARACTER", chars_OFFSET)

def getStat():
    displayMenu("STAT", stats_OFFSET)
    return validate("STAT", stats_OFFSET)

def getDec(char, thing, things_MAXVAL):
    dec = -1
    max = things_MAXVAL[thing]
    while dec not in range(0, max+1):
        if char == "all" and thing == "all":
            dec = int(input("Enter a new value for " +
                             thing.upper() + " STATS for " + char.upper() + " CHARACTERS"
                             " (0-" + str(max) + "): "))
        elif char == "all":
            dec = int(input("Enter a new value for " +
                             thing.upper() + " for " + char.upper() + " CHARACTERS"
                             " (0-" + str(max) + "): "))
        elif thing == "all":
            dec = int(input("Enter a new value for " +
                             thing.upper() + " STATS for " + char.upper() +
                             " (0-" + str(max) + "): "))
        else:
            dec = int(input("Enter a new value for " +
                            char.upper() + "'s " + thing.upper() +
                            " (0-" + str(max) + "): "))
    return dec

def validate(thing_TYPE, things_OFFSET):
    selection = 0
    numOfOptions = len(things_OFFSET)+1
    while selection not in range(1, numOfOptions):
        selection = int(input("Select a " + thing_TYPE.upper() + " (1-" + str(numOfOptions) + "): "))
        if selection == numOfOptions:
            break
    if selection == numOfOptions:
        return "all"
    pos = 1
    for thing in things_OFFSET:
        if pos == selection:
            return thing
        pos += 1

def displayChar(file, char):
    if char == "all":
        displayChars(file)
    else:
        print("----- (" + char.upper() + ") --------------")
        for stat in stats_OFFSET:
            if len(stats_OFFSET[stat]) == 2:
                print("\t" + stat.upper() + ": " + str(readBytes(file, chars_OFFSET[char] + stats_OFFSET[stat][0], 2)))
            else:
                print("\t" + stat.upper() + ": " + str(readByte(file, chars_OFFSET[char] + stats_OFFSET[stat][0])))
        print("-------------------------------")

def displayChars(file):
    for char in chars_OFFSET:
        print("----- (" + char.upper() + ") --------------")
        for stat in stats_OFFSET:
            if len(stats_OFFSET[stat]) == 2:
                print("\t" + stat.upper() + ": " + str(readBytes(file, chars_OFFSET[char] + stats_OFFSET[stat][0], 2)))
            else:
                print("\t" + stat.upper() + ": " + str(readByte(file, chars_OFFSET[char] + stats_OFFSET[stat][0])))
        print("-------------------------------")


# keira: (MAIN) ********************************************************************************************************

filename = 'SAVED.GAM'
char = "goldfish"
run = True

while (run):
    # start of program
    print()
    displayChar(filename, char)

    print()
    print("\t 1. Change Stats \n" +
          "\t 2. Change Items \n" +
          "\t 3. View Diff. Character \n"
          "\t 4. Exit \n")
    option = getOption(4)
    print()

    if option == 1:
        char = getChar()
        stat = getStat()
        dec = getDec(char, stat, things_MAXVAL)

        if char == "all" and stat == "all":
            setALLStats4ALLChars(filename, dec)
        elif stat == "all":
            setALLStats(filename, char, dec)
        elif char == "all":
            setStat4ALLChars(filename, stat, dec)
        else:
            setStat(filename, char, stat, dec)

    elif option == 2:
        print() # TODO: Add CHANGE ITEMS functionality.

    elif option == 3:
        char = getChar()

    elif option == 4:
        run = False

# keira:  (END OF MAIN) ************************************************************************************************
