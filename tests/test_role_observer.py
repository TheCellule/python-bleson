#!/usr/bin/env python3

import unittest
import os, sys
from time import sleep


from bleson import get_provider
from bleson.core.types import BDAddress
from bleson.core.roles import Observer
from bleson.logger import log, set_level, DEBUG

SCANTIME = 5          # seconds

BLE_DEVICE_BDADDR=BDAddress(os.getenv('BLE_TESTDEVICE_0_BDADDR', None))
BLE_DEVICE_LOCALNAME=os.getenv('BLE_TESTDEVICE_0_LOCALNAME', None)

class TestRoles(unittest.TestCase):

    def __init__(self, _):
        super().__init__(_)
        self.adapter = get_provider().get_adapter()
        # Turn on bleson DEBUG logging, keeping note of the previous setting.
        self.previous_log_level = set_level(DEBUG)

    def __del__(self):
        # Restore logging level, in case we're running in a test suite
        set_level(self.previous_log_level)

    def test_observer(self):

        found_devices = set()
        observer = Observer(self.adapter)

        def advertisement_update(advertisement):
            print("Advertisement.raw_data= {}".format(advertisement.raw_data))
            if sys.platform.lower().startswith('darwin'):
                found_devices.add(advertisement.name)
            else:
                found_devices.add(advertisement.address)

        observer.on_advertising_data = advertisement_update

        observer.start()
        log.info("Starting Observer role for {} seconds".format(SCANTIME))

        sleep(SCANTIME)
        observer.stop()

        log.info("Found: {}".format(found_devices))

        # TODO: revert this simple test, only in place for infrastructure testing
        self.assertTrue(len(found_devices)>0)
        # if sys.platform.lower().startswith('darwin'):
        #     self.assertTrue(BLE_DEVICE_LOCALNAME in found_devices)
        # else:
        #     self.assertTrue(BLE_DEVICE_BDADDR in found_devices)

