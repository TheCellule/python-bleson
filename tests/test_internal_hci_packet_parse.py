
import unittest

from bleson.core.hci import parse_hci_event_packet
from bleson.core.hci.type_converters import AdvertisingDataConverters
from bleson.logger import set_level, DEBUG
from bleson.utils import hexstring_to_bytearray

set_level(DEBUG)

EDDYSTONE_ADV_REPORT    = hexstring_to_bytearray('3e 21 02 01 00 00 1e ac e7 eb 27 b8 15 02 01 1a 03 03 aa fe 0d 16 aa fe 10 ed 00 67 6f 6f 67 6c 65 00 bc')
BBC_MICROBIT_ADV_REPORT = hexstring_to_bytearray('3e 26 02 01 00 01 f6 15 b0 c9 3a f5 1a 02 01 06 16 09 42 42 43 20 6d 69 63 72 6f 3a 62 69 74 20 5b 74 65 67 69 70 5d e4')
JSPUCK_ADV_REPORT       = hexstring_to_bytearray('3e 1d 02 01 00 01 43 7b 30 8e 58 f4 11 02 01 05 0d 09 50 75 63 6b 2e 6a 73 20 37 62 34 33 ac')
UUID128_ADV_REPORT      = hexstring_to_bytearray('3e 1d 02 01 04 01 43 7b 30 8e 58 f4 12 11 07 9e ca dc 24 0e e5 a9 e0 93 f3 a3 b5 01 00 40 6e')

class TestHCIParsers(unittest.TestCase):

    def test_parse_eddystone_advertisment_report(self):
        # Some context...
        # eddystone adv data = [
        #     0x02,  # Flags length
        #     0x01,  # Flags data type value
        #     0x1a,  # Flags data
        #
        #     0x03,  # Service UUID length
        #     0x03,  # Service UUID data type value
        #     0xaa,  # 16-bit Eddystone UUID
        #     0xfe,  # 16-bit Eddystone UUID
        #
        #     0x0d,     #5 + len(encodedurl),  # Service Data length
        #     0x16,  # Service Data data type value
        #     0xaa,  # 16-bit Eddystone UUID
        #     0xfe,  # 16-bit Eddystone UUID
        #
        #     0x10,  # Eddystone-url frame type
        #     0xed,  # txpower
        #
        #     0x00, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x00  # message += encode_url("http://www.google.com/")
        #     #from bleson.beacons.eddystone import EddystoneBeacon
        #     #log.info(hex_string(EddystoneBeacon.encode_url("http://www.google.com/")))
        #
        # ]

        # running : context_eddystone_beacon.py,
        # output from : sudo hcidump -i hci0 -X -R

        # > 0000: 04 3e 21 02 01 00 00 1e  ac e7 eb 27 b8 15 02 01  .>!........'....
        #   0010: 1a 03 03 aa fe 0d 16 aa  fe 10 ed 00 67 6f 6f 67  ............goog
        #   0020: 6c 65 00 bc                                       le..

        # hci_packet = '04 3e 21 02 01 00 00 1e ac e7 eb 27 b8 15 02 01 1a 03 03 aa fe 0d 16 aa fe 10 ed 00 67 6f 6f 67 6c 65 00 bc'
        # 04 is HCI_EVENT_PACKET type, one of a handful of types recevied by the Socket listener

        hci_packet = parse_hci_event_packet(EDDYSTONE_ADV_REPORT)

        advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)

        self.assertEqual(0x1a, advertisement.flags)
        self.assertEqual(-68, advertisement.rssi)
        self.assertEqual([bytearray([0xaa, 0xfe])], advertisement.uuid16s)
        self.assertEqual(b'\xaa\xfe\x10\xed\x00google\x00', advertisement.service_data)


    def test_parse_microbit_advertisment_report(self):

        hci_packet = parse_hci_event_packet( BBC_MICROBIT_ADV_REPORT)

        advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)

        self.assertEqual(0x06, advertisement.flags)
        self.assertEqual(-28, advertisement.rssi)
        self.assertEqual('BBC micro:bit [tegip]', advertisement.name)
        self.assertEqual(True, advertisement.name_is_complete)

    def test_parse_jspuck_advertisment_report(self):

        hci_packet = parse_hci_event_packet(JSPUCK_ADV_REPORT)

        advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)

        self.assertEqual(0x05, advertisement.flags)
        self.assertEqual(-84, advertisement.rssi)
        self.assertEqual('Puck.js 7b43', advertisement.name)
        self.assertEqual(True, advertisement.name_is_complete)

    def test_parse_jspuck_advertisment_report(self):

        hci_packet = parse_hci_event_packet(UUID128_ADV_REPORT)

        advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)

