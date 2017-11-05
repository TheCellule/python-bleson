import struct


from bleson.core.hci.constants import EVT_LE_META_EVENT
from .constants import HCI_EVENTS
from .types import HCIPacket

def event_to_string(event_code):
    return HCI_EVENTS[event_code]


def parse_hci_event_packet(data):
    evtcode, length = struct.unpack("<BB", data[:2])
    if evtcode != EVT_LE_META_EVENT:
        return HCIPacket(event_to_string(evtcode), evtcode, None, data[3:], length - 1)
    else:
        subevtcode = struct.unpack("<B", data[2:3])[0]
        return HCIPacket(event_to_string(evtcode), evtcode, subevtcode, data[3:], length-1)


def rssi_from_byte(rssi_unsigned):
    rssi =  rssi_unsigned - 256 if rssi_unsigned > 127 else rssi_unsigned
    if rssi == 127:
        rssi = None         # RSSI Not available
    elif rssi >=20:
        rssi = None         # Reserverd range 20-126

    return rssi