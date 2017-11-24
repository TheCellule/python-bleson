
import unittest

from bleson.core.types import UUID16, UUID128
from bleson.core.hci.type_converters import AdvertisingDataConverters, parse_hci_event_packet, hexstring_to_bytearray
from bleson.logger import log, set_level, DEBUG

EDDYSTONE_ADV_REPORT    = hexstring_to_bytearray('3e 21 02 01 00 00 1e ac e7 eb 27 b8 15 02 01 1a 03 03 aa fe 0d 16 aa fe 10 ed 00 67 6f 6f 67 6c 65 00 bc')
BBC_MICROBIT_ADV_REPORT = hexstring_to_bytearray('3e 26 02 01 00 01 f6 15 b0 c9 3a f5 1a 02 01 06 16 09 42 42 43 20 6d 69 63 72 6f 3a 62 69 74 20 5b 74 65 67 69 70 5d e4')
JSPUCK_ADV_REPORT       = hexstring_to_bytearray('3e 1d 02 01 00 01 43 7b 30 8e 58 f4 11 02 01 05 0d 09 50 75 63 6b 2e 6a 73 20 37 62 34 33 ac')
UUID128_ADV_REPORT      = hexstring_to_bytearray('3e 1d 02 01 04 01 43 7b 30 8e 58 f4 12 11 07 9e ca dc 24 0e e5 a9 e0 93 f3 a3 b5 01 00 40 6e')
BLUEFRUIT52_ADV_REPORT  = hexstring_to_bytearray('3e 19 02 01 04 00 ad af ad af ad af 0d 0c 09 42 6c 75 65 66 72 75 69 74 35 32 d6')

HEARTRATE_ADV_REPORT    = hexstring_to_bytearray('3e 29 02 01 00 01 3f 55 b5 74 6e 4e 1d 02 01 1a 05 03 0a 18 0d 18 0b 09 48 65 61 72 74 20 52 61 74 65 07 ff 4c 00 10 02 0b 00 c9')
THERMOMETER_ADV_REPORT  = hexstring_to_bytearray('3e 29 02 01 00 01 28 5f 74 ec 4f 6e 1d 02 01 1a 05 03 0a 18 09 18 13 09 48 65 61 6c 74 68 20 54 68 65 72 6d 6f 6d 65 74 65 72 b6')

NRF51X_LEGACY_DFU_ADV_REPORT = hexstring_to_bytearray('3e 28 02 01 00 01 bd ac 2c fb 4e 51 1c 02 01 1a 11 07 23 d1 bc ea 5f 78 23 15 de ef 12 12 30 15 00 00 06 09 6e 52 46 35 78 b9')


class TestHCIParsers(unittest.TestCase):

    def __init__(self, _):
        super().__init__(_)
        self.previous_log_level = set_level(DEBUG)

    def __del__(self):
        set_level(self.previous_log_level)



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
        self.assertEqual(True, UUID16(0xfeaa) in advertisement.uuid16s)
        self.assertEqual(1, len(advertisement.uuid16s))

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


    def test_parse_bluefruit52_advertisment_report(self):

        hci_packet = parse_hci_event_packet(BLUEFRUIT52_ADV_REPORT)
        advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)


    def test_parse_heartrate_advertisment_report(self):

        hci_packet = parse_hci_event_packet(HEARTRATE_ADV_REPORT)
        log.debug(hci_packet)
        advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)
        self.assertEqual(0x1a, advertisement.flags)
        self.assertEqual(-55, advertisement.rssi)
        self.assertEqual('Heart Rate', advertisement.name)
        self.assertEqual(True, advertisement.name_is_complete)
        self.assertEqual(True, UUID16(0x180a) in advertisement.uuid16s)
        self.assertEqual(True, UUID16(0x180d) in advertisement.uuid16s)
        self.assertEqual(2, len(advertisement.uuid16s))

    def test_parse_thermometer_advertisment_report(self):

        hci_packet = parse_hci_event_packet(THERMOMETER_ADV_REPORT)
        log.debug(hci_packet)
        advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)
        self.assertEqual(0x1a, advertisement.flags)
        self.assertEqual(-74, advertisement.rssi)
        self.assertEqual('Health Thermometer', advertisement.name)
        self.assertEqual(True, advertisement.name_is_complete)

        log.debug(advertisement.uuid16s)

        self.assertEqual(True, UUID16(0x180a) in advertisement.uuid16s)
        self.assertEqual(True, UUID16(0x1809) in advertisement.uuid16s)
        self.assertEqual(2, len(advertisement.uuid16s))


    def test_parse_nrf5x_lefacy_dfu_advertisement_report(self):

        hci_packet = parse_hci_event_packet(NRF51X_LEGACY_DFU_ADV_REPORT)
        log.debug(hci_packet)

        advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)
        self.assertEqual(0x1a, advertisement.flags)
        self.assertEqual(-71, advertisement.rssi)
        self.assertEqual('nRF5x', advertisement.name)
        log.debug(advertisement.uuid128s)
        self.assertEqual(True, UUID128('00001530-1212-efde-1523-785feabcd123') in advertisement.uuid128s)
        self.assertEqual(1, len(advertisement.uuid128s))