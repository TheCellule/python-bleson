#!/usr/bin/env python3

# This test expects the host to have 2 Bluetooth LE adapters available.
# e.g. a Pi3/ZeroW with a BluetoothLE USB dongle.

import unittest
from time import sleep

from bleson import get_provider
from bleson.core.types import Advertisement
from bleson.core.roles import Observer, Advertiser
from bleson.beacons.eddystone import EddystoneBeacon
from bleson.logger import log, set_level, DEBUG, INFO

import sys
TEST_DURATION_SECS = 5


class TestDualAdapters(unittest.TestCase):

    def __init__(self, _):
        super().__init__(_)

        self.previous_log_level = set_level(DEBUG)

        provider = get_provider()
        self.adapter0 = provider.get_adapter(0)  # Used for the Observer role
        self.adapter1 = provider.get_adapter(1)  # Used for the Advertiser role

        # Turn on bleson DEBUG logging, keeping note of the previous setting.

    def __del__(self):
        # Restore logging level, in case we're running in a test suite
        set_level(self.previous_log_level)


    def test_observer_advertiser_pair(self):

        # if not sys.platform.lower().startswith('linux'):
        #     raise unittest.SkipTest("Dual adapter tests only run on Linux")

        # ----------------------------------------
        # Setup the Observer, on adatper 0

        observer = Observer(self.adapter0)

        # The observer callback records the found device BDAddress

        found_addresses = set()

        def advertisement_update(advertisement):
            log.info("Found: {}".format(advertisement))
            found_addresses.add(advertisement.address)   # instance of 'BDAddress'

        observer.on_advertising_data = advertisement_update


        # ----------------------------------------
        # Setup the Advertiser, on adapter 1

        advertiser = Advertiser(self.adapter1)

        advertisement = Advertisement()
        advertisement.name = "bleson"

        advertiser.advertisement = advertisement


        # ----------------------------------------
        # Start the Observer and the Advertiser.

        observer.start()
        advertiser.start()

        # wait...
        log.info("Starting Advertiser & Observer roles for {} seconds, advertised name={}".format(TEST_DURATION_SECS, advertisement.name))

        sleep(TEST_DURATION_SECS)

        # Stop
        advertiser.stop()
        observer.stop()


        # ----------------------------------------
        # Did the left hand find the right hand?

        log.info("Observer's   address: {}".format(self.adapter0.device.address))
        log.info("Advertiser's address: {}".format(self.adapter1.device.address))
        log.info("Observed BDAddresses: {}".format(found_addresses))

        self.assertTrue(self.adapter1.device.address in found_addresses)



    def test_observer_beacon_pair(self):

        # if not sys.platform.lower().startswith('linux'):
        #     raise unittest.SkipTest("Dual adapter tests only run on Linux")

        observer = Observer(self.adapter0)
        found_addresses = set()

        def advertisement_update(advertisement):
            log.info("Found: {}".format(advertisement))
            found_addresses.add(advertisement.address)   # instance of 'BDAddress'

        observer.on_advertising_data = advertisement_update

        beacon = EddystoneBeacon(self.adapter1)


        # ----------------------------------------
        # Start the Observer and the Advertiser.

        observer.start()
        beacon.start()

        # wait...
        log.info("Starting Advertiser & Observer roles for {} seconds, advertised url={}".format(TEST_DURATION_SECS, beacon.url))

        sleep(TEST_DURATION_SECS)

        # Stop
        beacon.stop()
        observer.stop()


        # ----------------------------------------
        # Did the left hand find the right hand?

        log.info("Observer's address: {}".format(self.adapter0.device.address))
        log.info("Beacons's  address: {}".format(self.adapter1.device.address))
        log.info("Observed BDAddresses: {}".format(found_addresses))

        self.assertTrue(self.adapter1.device.address in found_addresses)
