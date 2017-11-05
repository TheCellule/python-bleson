import struct
from collections import namedtuple

from bleson import log

HCIPacket = namedtuple('HCIPacket', 'event_name event_code subevent_code data length')


class HCIPayload:

    def __init__(self, with_data=b''):
        self.data = bytes(with_data)
        self._parse_data()

    def add_item(self, tag, value):
        log.debug("'{}' = {}".format(tag, value))
        newdata = self.data + struct.pack("<BB", 1+len(value), tag) + bytes(value)
        log.debug(newdata)
        if len(newdata) <= 31:
            self.data = newdata
            self.tags[tag] = value
        else:
            raise IndexError("Supplied advertising data too long (%d bytes total)", len(newdata))
        return self

    def __iter__(self):
        '''Use: for (tag,value) in obj:'''
        ofs = 0
        maxlen = len(self.data)
        while ofs < maxlen:
            if maxlen - ofs < 2:
                raise IndexError("Advertising data too short")
            (ll, tag) = struct.unpack("<BB", self.data[ofs:ofs+2])
            if ll==0 or ofs+1+ll > maxlen:
                raise IndexError("Bad length byte 0x%02X in advertising data" % ll)
            yield (tag, self.data[ofs+2:ofs+1+ll])
            ofs = ofs + 1 + ll

    def _parse_data(self):
        self.tags={}
        for (tag,value) in self:
            self.tags[tag] = value

    def __str__(self):
        return repr(self.tags) # TODO...