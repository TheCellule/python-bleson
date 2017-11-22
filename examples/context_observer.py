#!/usr/bin/env python3

import sys
from time import sleep
from bleson import get_provider, Observer
from bleson.logger import log, set_level, DEBUG

#set_level(DEBUG)


# Get the wait time from the first script argument or default it to 10 seconds
WAIT_TIME = int(sys.argv[1]) if len(sys.argv)>1 else 10

with Observer(get_provider().get_adapter(), lambda device: log.info(device)):
    sleep(WAIT_TIME)

