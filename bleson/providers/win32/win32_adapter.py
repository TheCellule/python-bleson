import threading
from bleson.interfaces.adapter import Adapter
from bleson.core.types import Advertisement, UUID16, UUID128, BDAddress
from bleson.core.hci.constants import *
from bleson.logger import log
from bleson.core.hci.type_converters import bytearray_to_hexstring

# Work around for Sphinx
try:
    import blesonwin
except (ImportError, AttributeError) as e:
    import sys
    if 'sphinx' in sys.modules:
        log.warning("blesonwin not found, if this is a documentation build all is good")
    else:
        log.error("blesonwin not found, but this doesn't look like a documentation build")
        raise e

    blesonwin = {}


class BluetoothAdapter(Adapter):

    def __init__(self, device_id=0):
        self.device_id = device_id
        self.connected = False
        self._keep_running = True
        self.on_advertising_data = None
        blesonwin.initialise()


    def open(self):
        pass


    def on(self):
        log.debug("TODO: adatper on")

    def off(self):
        log.debug("TODO: adatper off")

    def start_scanning(self):
        log.info("start scanning")
        if self.on_advertising_data:
            blesonwin.on_advertisement(self._on_advertising_data)
        else:
            log.warning("on_advertising_data is not set")

        log.info(self.on_advertising_data)
        blesonwin.start_observer()

    def stop_scanning(self):
        log.info("stopping")
        blesonwin.stop_observer()

    def start_advertising(self, advertisement, scan_response=None):
        log.debug("TODO: pass user adv data")
        blesonwin.start_advertiser()

    def stop_advertising(self):
        blesonwin.stop_advertiser()

    def _on_advertising_data(self, data):
        try:
            log.debug('Found: {}'.format(data))

            if self.on_advertising_data:
                advertisement = Advertisement()
                advertisement.flags = 0
                advertisement.rssi = data['RSSI']

                if 'ADDRESS' in data:
                    advertisement.address = BDAddress(data['ADDRESS'])

                if 'LOCALNAME' in data:
                    advertisement.name = data['LOCALNAME']

                if 'TXPOWER' in data:
                    advertisement.tx_pwr_lvl = int(data['TXPOWER'])

                self.on_advertising_data(advertisement)

        except Exception as e:
            log.exception(e)