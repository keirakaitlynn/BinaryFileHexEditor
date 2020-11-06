
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


offsets = {
    "strength":     [0x000E],
    "intelligence": [0x000F],
    "dexterity":    [0x0010],
    "magic":        [0x0011],
    "hp":           [0x0012, 0x0013],
    "hm":           [0x0014, 0x0015],
    "experience":   [0x0016, 0x0017],
    "gold":         [0x0204, 0x0205]
}


# keira:  (SAVED.GAM methods) ------------------------------------------------------------------------------------------
def setByte(file, offset, dec):
    byte_array = byteArrayOf(littleEndianOf(hexOf(dec)))

    # 'rb': used to open & read file as a binary file, so that the bytes of the file won't be encoded when read
    with open(file, 'r+b') as file:
        file.seek(offset)
        # assert file.tell() == 0x000E
        file.write(byte_array)

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

for x in offsets:
    dec = int(input("Enter in a value for " + x + ": "))
    setByte(filename, offsets[x][0], dec)

dec = 999
byte_array = byteArrayOf(littleEndianOf(hexOf(dec)))
print(byte_array)

# 'rb': used to open & read file as a binary file, so that the bytes of the file won't be encoded when read
# with open(filename, 'r+b') as file:
#     file.seek(offsets["hp"])
#     # assert file.tell() == 0x000E
#     file.write(byte_array)
#
# (END OF MAIN) ----------
