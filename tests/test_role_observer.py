#!/usr/bin/env python3

import unittest
from time import sleep


from bleson import get_provider
from bleson.core.types import BDAddress
from bleson.core.roles import Observer
from bleson.logger import log, set_level, DEBUG

SCANTIME = 5          # seconds

MICROBIT1_BDADDR=BDAddress('f5:3a:c9:b0:15:f6')


class TestRoles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.adapter = get_provider().get_adapter()
        # Turn on bleson DEBUG logging, keeping note of the previous setting.
        cls.previous_log_level = set_level(DEBUG)

    @classmethod
    def tearDownClass(cls):
        # Restore logging level, in case we're running in a test suite
        set_level(cls.previous_log_level)

    def test_observer(self):

        found_devices = set()
        observer = Observer(self.adapter)

        def advertisement_update(advertisement):
            found_devices.add(advertisement.address)

        observer.on_advertising_data = advertisement_update

        observer.start()
        log.info("Starting Observer role for {} seconds".format(SCANTIME))

        sleep(SCANTIME)
        observer.stop()

        log.info("Found: {}".format(found_devices))

        self.assertTrue(MICROBIT1_BDADDR in found_devices)

