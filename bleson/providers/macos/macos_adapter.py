from bleson.interfaces.adapter import Adapter
from bleson.core.types import Advertisement
from bleson.logger import log

import objc
from PyObjCTools import AppHelper
objc.loadBundle("CoreBluetooth", globals(),
                bundle_path=objc.pathForFramework(
                    u'/System/Library/Frameworks/IOBluetooth.framework/Versions/A/Frameworks/CoreBluetooth.framework'))


class CoreBluetoothAdapter(Adapter):

    def __init__(self, device_id=0):
        self.device_id = device_id
        self.connected = False
        self._keep_running = True
        self._manager = CBCentralManager.alloc()


    def open(self):
        self._manager.initWithDelegate_queue_options_(self, None, None)


    def on(self):
        log.warn("TODO: adatper on")

    def off(self):
        log.warn("TODO: adatper off")

    def start_scanning(self):
        log.info("start scanning")
        try:
            AppHelper.runConsoleEventLoop(installInterrupt=True)
        except KeyboardInterrupt:
            AppHelper.stopEventLoop()

    def stop_scanning(self):
        self.manager.stopScan()
        #self.peripheral = peripheral
        #manager.connectPeripheral_options_(self.peripheral, None)

    def start_advertising(self, advertisement, scan_response=None):
        raise NotImplementedError

    def stop_advertising(self):
        raise NotImplementedError


    # CoreBluetooth Protocol

    def centralManagerDidUpdateState_(self, manager):
        log.debug("centralManagerDidUpdateState_")

        if self.connected == False:
            self.manager = manager
            manager.scanForPeripheralsWithServices_options_(None, None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        log.debug("centralManager_didDiscoverPeripheral_advertisementData_RSSI_")
        log.debug('Found: name={} rssi={} data={} '.format(peripheral.name(), rssi, data))

        if self.on_advertising_data:
            advertisement = Advertisement()
            advertisement.name = peripheral.name()
            advertisement.rssi = rssi
            self.on_advertising_data(advertisement)


    def centralManager_didConnectPeripheral_(self, manager, peripheral):
        log.debug("centralManager_didConnectPeripheral_")
        log.debug('Connected: ' + peripheral.name())
        self.connected = True
        self.peripheral.setDelegate_(self)
        self.peripheral.readRSSI()
        #self.peripheral.discoverServices_([CBUUID(...)])

    def centralManager_didFailToConnectPeripheral_error_(self, manager, peripheral, error):
        log.debug("centralManager_didFailToConnectPeripheral_error_")

        log.error(repr(error))

    def centralManager_didDisconnectPeripheral_error_(self, manager, peripheral, error):
        log.debug("centralManager_didDisconnectPeripheral_error_")
        self.connected = False
        AppHelper.stopEventLoop()

    def peripheral_didDiscoverServices_(self, peripheral, error):
        log.debug("peripheral_didDiscoverServices_")
        if (error == None):
            self.service = self.peripheral.services()[0]
            #self.peripheral.discoverCharacteristics_forService_([CBUUD(...)], self.service)

    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
        log.debug("peripheral_didDiscoverCharacteristicsForService_error_")

        for characteristic in self.service.characteristics():
            if characteristic.UUID().UUIDString() == crtp_characteristic.UUIDString():
                self.crtp_characteristic = characteristic
                self.peripheral.setNotifyValue_forCharacteristic_(True, self.crtp_characteristic)

    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        log.debug("peripheral_didWriteValueForCharacteristic_error_")

        if error != None:
            log.error(repr(error))

    def peripheral_didUpdateNotificationStateForCharacteristic_error_(self, peripheral, characteristic, error):
        log.debug("peripheral_didUpdateNotificationStateForCharacteristic_error_")


    def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
        log.debug("peripheral_didUpdateValueForCharacteristic_error_")
        repr(characteristic.value().bytes().tobytes())
