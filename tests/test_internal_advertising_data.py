import unittest

from bleson.logger import log, set_level, DEBUG
from bleson.core.types import Advertisement

from bleson.core.hci.type_converters import  AdvertisingDataConverters

set_level(DEBUG)

class TestAdvertisingData(unittest.TestCase):


    def test_create_hcipayload_from_advertising(self):

        adv = Advertisement()
        adv.name = 'blename'
        log.info(adv.raw_data)

        hci_payload = AdvertisingDataConverters.from_advertisement(adv)
        log.info(hci_payload)

        self.assertEqual(b'\x02\x01\x06\x08\x09blename', hci_payload)

