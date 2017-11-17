#!/usr/bin/env python3

import sys
from time import sleep
from bleson import get_provider, EddystoneBeacon

# Get the wait time from the first script argument or default it to 10 seconds
WAIT_TIME = int(sys.argv[1]) if len(sys.argv)>1 else 10

with EddystoneBeacon(get_provider().get_adapter(), 'https://www.bluetooth.com/'):
    sleep(WAIT_TIME)
