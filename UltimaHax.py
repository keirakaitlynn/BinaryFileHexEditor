
# XXXXX: (fix ASAP!)
# KEIRA: (main headers)
# kkkkk: (sub-headers)
# KKKKK: (sub sub-headers)

# TODO: (incomplete)
# QUESTION: (wtf did i just do)


# KEIRA: (Offsets) **************

# kkkkk:  (CHAR STATS)  ---------
# Strength:     (0x000C)
# Intelligence: (0x000D)
# Dexterity:    (0x000E)
# Magic:        (0x000F)
# HP:           (0x0010) (0x0011)
# HM:           (0x0012) (0x0013)
# Experience:   (0x0014) (0x0015)
# Gold:         (0x0204) (0x0205)

# kkkkk: (CHAR STATS)
# Strength:     (0x000E)
# Intelligence: (0x000F)
# Dexterity:    (0x0010)
# Magic:        (0x0011)
# HP:           (0x0012) (0x0013)
# HM:           (0x0014) (0x0015)
# Experience:   (0x0016) (0x0017)
# Gold:         (0x0204) (0x0205)


stats_OFFSET = {
    "strength":     [0x000E],
    "intelligence": [0x000F],
    "dexterity":    [0x0010],
    "magic":        [0x0011],
    "hp":           [0x0012, 0x0013],
    "hm":           [0x0014, 0x0015],
    "experience":   [0x0016, 0x0017],
    "gold":         [0x0204, 0x0205]
}

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


# keira:  (SAVED.GAM methods) ------------------------------------------------------------------------------------------
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

def setStat(char, stat, dec):
    setByte(filename, chars_OFFSET[char] + stats_OFFSET[stat][0], dec)

def setStats(file, char, stat, dec):
    print("------- (" + char.upper() + ") --------------------------------")
    for stat in stats_OFFSET:
        dec = int(input("Enter in a value for " + stat.upper() + ": "))
        setByte(file, chars_OFFSET[char] + stats_OFFSET[stat][0], dec)
    print("--------------------------------------------------")

def setStats4AllChars(file, chars_OFFSET, stats_OFFSET):
    for char in chars_OFFSET:
        print("------- (" + char.upper() + ") --------------------------------")
        for stat in stats_OFFSET:
            dec = int(input("Enter in a value for " + stat.upper() + ": "))
            setByte(file, chars_OFFSET[char] + stats_OFFSET[stat][0], dec)
        print("--------------------------------------------------")

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


# keira: (MAIN) ********************************************************************************************************

filename = 'SAVED.GAM'

setStats4AllChars(filename, chars_OFFSET, stats_OFFSET)


# keira:  (END OF MAIN) ************************************************************************************************
