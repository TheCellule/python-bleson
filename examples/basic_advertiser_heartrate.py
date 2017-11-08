#!/usr/bin/env python3

import sys
from time import sleep

from bleson.logger import log, set_level, DEBUG
from bleson import get_provider, Advertiser, Advertisement, UUID16, LE_GENERAL_DISCOVERABLE, BREDR_NOT_SUPPORTED

previous_log_level = set_level(DEBUG)
# Get the wait time from the first script argument or default it to 10 seconds
WAIT_TIME = int(sys.argv[1]) if len(sys.argv)>1 else 10

adapter = get_provider().get_adapter()

advertiser = Advertiser(adapter)

advertisement = Advertisement()
advertisement.name = "Heart Rate"
advertisement.flags = LE_GENERAL_DISCOVERABLE | BREDR_NOT_SUPPORTED
advertisement.uuid16s = [UUID16(0x180a), UUID16(0x180d)]

advertiser.advertisement = advertisement

advertiser.start()
sleep(WAIT_TIME)
advertiser.stop()

set_level(previous_log_level)