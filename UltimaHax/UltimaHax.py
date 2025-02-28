

# this program must be placed in the same file as the SAVED.GAM to edit.


# XXXXX:     (fix ASAP!)          (#c6001a)
# KEIRA:     (main headers)       (#ff0070)
# kkkkk:     (sub-headers)        (#fcb9c5)
# KKKKK:     (sub sub-headers)    (#b97474)
# TODO:      (incomplete)         (#ccff00)
# QUESTION:  (review later)       (#00b9ff)


# KEIRA: (OFFSETs) -----------------------------------------------------------------------------------------------------

chars_OFFSET = {
    "KEIRA": 0x0000,
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
}

items_OFFSET = {
    "gold":  [0x0204, 0x0205],
    "keys":          [0x0206],
    "skull keys":    [0x020B],
    "gems":          [0x0207],
    "black badges":   [0x0218],
    "magic carpets": [0x020A],
    "magic axes":    [0x0240]
}

things_MAXVAL = {
    "strength":      255,
    "intelligence":  255,
    "dexterity":     255,
    "magic":         255,
    "hp":          65535,
    "max hp":      65535,
    "experience":  65535,

    # FFFF (65535)  = max. dec val for 2 bytes
    # FF   (255)    = max. dec val for 1 byte

    "gold":        65535,
    "keys":          255,
    "skull keys":    255,
    "gems":          255,
    "black badges":   255,
    "magic carpets": 255,
    "magic axes":    255,
    "all":           255
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

    # 'r+b': used to...
    #        - open & read file ('r')
    #        - read file as a binary file, so that the bytes of the file won't be encoded when read ('b')
    #        - overwrite data, rather than truncate the rest ('+')

    with open(file, 'r+b') as file:
        file.seek(offset)
        # assert file.tell() == 0x000E
        file.write(byte_array)

# kkkkk: Given char, stat & dec, sets stat of char to dec.
def setStat(file, char, stat, dec):
    if len(stats_OFFSET[stat]) == 2:
        setBytes(file, chars_OFFSET[char] + stats_OFFSET[stat][0], dec)
    elif len(stats_OFFSET[stat]) == 1:
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

def setItem(file, item, dec):
    if len(items_OFFSET[item]) == 2:
        setBytes(file, items_OFFSET[item][0], dec)
    elif len(items_OFFSET[item]) == 1:
        setByte(file, items_OFFSET[item][0], dec)

def setALLItems(file, dec):
    for item in items_OFFSET:
        setItem(file, item, dec)


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

def getItem():
    displayMenu("ITEM", items_OFFSET)
    return validate("ITEM", items_OFFSET)

def getDec(char, thing, things_MAXVAL):
    dec = -1
    max = things_MAXVAL[thing]
    while dec not in range(0, max+1):
        if char == "n/a" and thing == "all":
            dec = int(input("Enter a new value for " +
                             thing.upper() + " ITEMS" +
                             " (0-" + str(max) + "): "))
        elif char == "n/a":
            dec = int(input("Enter a new value for " +
                             thing.upper() + " " +
                             " (0-" + str(max) + "): "))
        elif char == "all" and thing == "all":
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

def setDefaultValues(file):
    setALLStats4ALLChars(file, 99)
    setStat4ALLChars(file, "hp", 999)
    setStat4ALLChars(file, "max hp", 999)
    setStat4ALLChars(file, "experience", 9999)
    setALLItems(file, 100)
    setItem(file, "gold", 9999)
    setItem(file, "black badges", 1)
    setItem(file, "magic carpets", 2)
    setItem(file, "magic axes", 10)
    displayChars(file)

def displayThing(file, char, thing_TYPE, things_OFFSET):
    header = thing_TYPE.upper() + "S"
    char_OFFSET = 0
    if char != "n/a":
        header = char.upper()
        char_OFFSET = chars_OFFSET[char]
    print("----- (" + header + ") --------------")
    for thing in things_OFFSET:
        if len(things_OFFSET[thing]) == 2:
            print("\t" + thing.lower() + ": " + str(readBytes(file, char_OFFSET + things_OFFSET[thing][0], 2)))
        else:
            print("\t" + thing.lower() + ": " + str(readByte(file, char_OFFSET + things_OFFSET[thing][0])))
    print("-------------------------------")

# "all" or "n/a": if char is "all", will print stats for each char (w/ char.upper() as header)
#                 if char is "n/a", will just print a list of things (w/ thing.upper as header)
# "thing" & "things_OFFSET": a stat or item & its corresponding list of OFFSETs
def displayThings(file, char, thing_TYPE, things_OFFSET):
    if char == "all":
        for char in chars_OFFSET:
            displayThing(file, char, thing_TYPE, things_OFFSET)
    else:
        displayThing(file, char, thing_TYPE, things_OFFSET)

def displayItems(file):
    displayThing(file, "n/a", "item", items_OFFSET)

def displayChar(file, char):
    if char == "all":
        displayChars(file)
    else:
        displayThing(file, char, "stat", stats_OFFSET)

def displayChars(file):
    displayThings(file, "all", "stat", stats_OFFSET)


# keira: (MAIN) ********************************************************************************************************

file = 'SAVED.GAM'
char = "KEIRA"
item = "gold"
run = True

while (run):
    # start of program
    print()
    displayChar(file, char)
    displayItems(file)

    print()
    print("\t 1. Change Stats \n" +
          "\t 2. Change Items \n" +
          "\t 3. View a Diff. Char \n" +
          "\t 4. Set Default Values \n" +
          "\t 5. Exit \n")
    option = getOption(5)
    print()

    if option == 1:
        char = getChar()
        displayChar(file, char)
        stat = getStat()
        dec = getDec(char, stat, things_MAXVAL)

        if char == "all" and stat == "all":
            setALLStats4ALLChars(file, dec)
        elif stat == "all":
            setALLStats(file, char, dec)
        elif char == "all":
            setStat4ALLChars(file, stat, dec)
        else:
            setStat(file, char, stat, dec)

    elif option == 2:
        displayItems(file)
        item = getItem()
        dec = getDec("n/a", item, things_MAXVAL)

        if item == "all":
            setALLItems(file, dec)
        else:
            setItem(file, item, dec)

    elif option == 3:
        char = getChar()

    elif option == 4:
        setDefaultValues(file)

    elif option == 5:
        run = False

# keira: (END OF MAIN) ************************************************************************************************