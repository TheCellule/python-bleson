#!/usr/bin/env python3

import unittest
from time import sleep

from bleson import get_provider
from bleson.core.types import BDAddress, Advertisement
from bleson.core.roles import Advertiser
from bleson.logger import log

ADVERTISE_TIME = 5      # seconds

MICROBIT1_BDADDR=BDAddress('f5:3a:c9:b0:15:f6')


class TestAdvertiser(unittest.TestCase):

    def test_advertiser(self):
        adapter = get_provider().get_adapter()

        advertisement = Advertisement()
        advertisement.name = 'bleson'

        advertiser = Advertiser(adapter)
        advertiser.advertisement = advertisement

        advertiser.start()
        log.info("Starting Advertiser role for {} seconds, advertised name={}".format(ADVERTISE_TIME, advertisement.name))

        sleep(ADVERTISE_TIME)
        advertiser.stop()

