import binascii

def hex_string(data):
    return ''.join('{:02x} '.format(x) for x in data)

def bytearray_to_hexstring(ba):
    return hex_string(ba)
    #return binascii.hexlify(ba)

def hexstring_to_bytearray(hexstr):
    """"
        hexstr:     e.g. de ad be ef 00"
    """
    return bytearray.fromhex(hexstr)
