import unittest

from bleson.logger import log, set_level, DEBUG
from bleson.core.types import Advertisement, UUID16, UUID128

from bleson.core.hci.type_converters import  AdvertisingDataConverters, hexstring_to_bytearray

set_level(DEBUG)

class TestAdvertisingData(unittest.TestCase):


    def test_create_adv_name(self):

        adv = Advertisement()
        adv.name = 'blename'

        hci_payload = AdvertisingDataConverters.from_advertisement(adv)
        log.info(hci_payload)

        self.assertEqual(adv.raw_data, None)
        self.assertEqual(b'\x02\x01\x06\x08\x09blename', hci_payload)


    def test_create_adv_uuid16_single(self):

        adv = Advertisement()
        adv.name = 'blename'
        adv.uuid16s = [UUID16(0xfeff)]


        hci_payload = AdvertisingDataConverters.from_advertisement(adv)
        log.info(hci_payload)

        self.assertEqual(adv.raw_data, None)
        self.assertEqual(b'\x02\x01\x06\x03\x03\xff\xfe\x08\x09blename', hci_payload)


    def test_create_adv_uuid128_single(self):
        NRF51X_LEGACY_DFU_ADV_DATA = hexstring_to_bytearray(
            '02 01 1a 11 07 23 d1 bc ea 5f 78 23 15 de ef 12 12 30 15 00 00 06 09 6e 52 46 35 78')

        adv = Advertisement()
        adv.flags = 0x1a
        adv.name  = 'nRF5x'
        adv.uuid128s = [ UUID128('00001530-1212-efde-1523-785feabcd123')]

        hci_payload = AdvertisingDataConverters.from_advertisement(adv)
        log.info(hci_payload)

        self.assertEqual(adv.raw_data, None)
        self.assertEqual(NRF51X_LEGACY_DFU_ADV_DATA, hci_payload)