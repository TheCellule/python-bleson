#!/usr/bin/env python3

import sys
from time import sleep
from bleson import get_provider, Observer

# Get the wait time from the first script argument or default it to 10 seconds
WAIT_TIME = int(sys.argv[1]) if len(sys.argv)>1 else 10


def on_advertisement(advertisement):
    print(advertisement)

adapter = get_provider().get_adapter()

observer = Observer(adapter)
observer.on_advertising_data = on_advertisement

observer.start()
sleep(WAIT_TIME)
observer.stop()

