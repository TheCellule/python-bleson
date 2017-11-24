#!/usr/bin/env python3

import unittest
from time import sleep

from bleson import get_provider
from bleson.beacons.eddystone import EddystoneBeacon
from bleson.logger import log

BEACON_TIME = 10

class TestBeacons(unittest.TestCase):

    def test_eddystone(self):
        adapter = get_provider().get_adapter()
        beacon = EddystoneBeacon(adapter, 'https://www.google.com/')
        beacon.start()
        log.info("Starting beacon for {} seconds, url={}".format(BEACON_TIME, beacon.url))
        sleep(BEACON_TIME)
        beacon.stop()
