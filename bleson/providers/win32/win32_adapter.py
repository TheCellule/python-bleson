import threading
from bleson.interfaces.adapter import Adapter
from bleson.core.types import Advertisement, UUID16, UUID128
from bleson.core.hci.constants import *
from bleson.logger import log
from bleson.core.hci.type_converters import bytearray_to_hexstring

#Minimum version for BLE scanning without paring and GATT Peripheral :  https://docs.microsoft.com/en-gb/windows/uwp/whats-new/windows-10-build-15063


#https://docs.microsoft.com/en-gb/uwp/api/windows.devices.bluetooth.genericattributeprofile.gattserviceprovider
#https://docs.microsoft.com/en-gb/uwp/api/windows.devices.bluetooth.bluetoothledevice


class BluetoothAdapter(Adapter):

    def __init__(self, device_id=0):
        self.device_id = device_id
        self.connected = False
        self._keep_running = True


    def open(self):
        pass


    def on(self):
        log.warn("TODO: adatper on")

    def off(self):
        log.warn("TODO: adatper off")

    def start_scanning(self):
        log.info("start scanning")

    def stop_scanning(self):
        log.info("stopping")

    def start_advertising(self, advertisement, scan_response=None):
        raise NotImplementedError

    def stop_advertising(self):
        raise NotImplementedError

