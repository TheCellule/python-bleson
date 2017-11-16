import threading
from bleson.interfaces.adapter import Adapter
from bleson.core.types import Advertisement, UUID16, UUID128
from bleson.core.hci.constants import *
from bleson.logger import log
from bleson.core.hci.type_converters import bytearray_to_hexstring

import blesonwin

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
        log.warn("TODO: adatper on")

    def off(self):
        log.warn("TODO: adatper off")

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
        raise NotImplementedError

    def stop_advertising(self):
        raise NotImplementedError

    def _on_advertising_data(self, data):
        try:
            log.debug('Found: {}'.format(data))

            if self.on_advertising_data:
                advertisement = Advertisement()
                advertisement.flags = 0
                advertisement.rssi = data['RSSI']

                if 'LOCALNAME' in data:
                    advertisement.name = int(data['LOCALNAME'])

                if 'TXPOWER' in data:
                    advertisement.tx_pwr_lvl = int(data['TXPOWER'])

                self.on_advertising_data(advertisement)

        except Exception as e:
            log.exception(e)