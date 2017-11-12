import threading
from bleson.interfaces.adapter import Adapter
from bleson.core.types import Advertisement, UUID16, UUID128
from bleson.core.hci.constants import *
from bleson.logger import log
from bleson.core.hci.type_converters import bytearray_to_hexstring
import objc
from Foundation import *
from PyObjCTools import AppHelper
import CoreBluetooth

# https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/Multithreading/RunLoopManagement/RunLoopManagement.html

# pyobjc:  https://bitbucket.org/ronaldoussoren/pyobjc
# https://bitbucket.org/ronaldoussoren/pyobjc/src/87ce46672615ef127f40850cc78401ca62cc336a/pyobjc-framework-CoreBluetooth/PyObjCTest/?at=default

# Issue: https://bitbucket.org/ronaldoussoren/pyobjc/issues/215/starting-runconsoleeventloop-from-a

# ObjC diest support dispatchQueues...

# use XPC instead:  https://github.com/sandeepmistry/noble/blob/master/lib/mac/yosemite.js



# Python XPC

# brew install python3
# brew install boost-python --with-python3
# ln -s /usr/local/lib/libboost_python3.a /usr/local/lib/libboost_python-py34.a
# git clone https://github.com/matthewelse/pyxpcconnection
# cd pyxpcconnection
# edit setup.py:
"""
-        extra_compile_args=['-std=c++11'],
+        extra_compile_args=['-std=c++11', '-stdlib=libc++', '-mmacosx-version-min=10.9'],
         libraries = boost_libs
"""
# python3 setup.py install



class CoreBluetoothAdapter(Adapter):

    def __init__(self, device_id=0):
        self.device_id = device_id
        self.connected = False
        self._keep_running = True
        self._socket_poll_thread = threading.Thread(target=self._runloop_thread, name='BlesonObjCRunLoop')
        self._socket_poll_thread.setDaemon(True)
        self._manager = None

    def open(self):
        pass


    def on(self):
        log.warn("TODO: adatper on")

    def off(self):
        log.warn("TODO: adatper off")

    def start_scanning(self):
        log.info("start scanning")
        self._runloop_thread()
        #self._socket_poll_thread.start()


    def stop_scanning(self):
        log.info("stopping")
        rc = AppHelper.stopEventLoop()
        log.info("done: AppHelper.stopEventLoop, successful?={}".format(rc))

    def start_advertising(self, advertisement, scan_response=None):
        raise NotImplementedError

    def stop_advertising(self):
        raise NotImplementedError

    # Obj Runloop

    def _init_cb_manager(self):
        # objc.loadBundle("CoreBluetooth", globals(),
        #                 bundle_path=objc.pathForFramework(
        #                     u'/System/Library/Frameworks/IOBluetooth.framework/Versions/A/Frameworks/CoreBluetooth.framework'))

        self._manager = CoreBluetooth.CBCentralManager.alloc()
        self._manager.initWithDelegate_queue_options_(self, None, None)

    # https://pythonhosted.org/pyobjc/core/intro.html#working-with-threads
    def _runloop_thread(self):
        try:
            log.info('AppHelper.runConsoleEventLoop()')
            pool = NSAutoreleasePool.alloc().init()
            self._init_cb_manager()
            rc = AppHelper.runConsoleEventLoop(installInterrupt=True)
            log.info(rc)
        except Exception as e:
            log.exception(e)
        finally:
            AppHelper.stopEventLoop()
            del pool
        log.info("leaving")

    # CoreBluetooth Protocol

    def centralManagerDidUpdateState_(self, manager):
        log.debug("centralManagerDidUpdateState_")

        if self.connected == False:
            self.manager = manager
            manager.scanForPeripheralsWithServices_options_(None, None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        try:
            log.debug("centralManager_didDiscoverPeripheral_advertisementData_RSSI_")
            log.debug('Found: name={} rssi={} data={} '.format(peripheral.name(), rssi, data))

            if self.on_advertising_data:
                advertisement = Advertisement()
                advertisement.flags = 0                  # Not available
                advertisement.name = peripheral.name()
                advertisement.rssi = rssi

                if 'kCBAdvDataTxPowerLevel' in data:
                    advertisement.tx_pwr_lvl = int(data['kCBAdvDataTxPowerLevel'])

                if data['kCBAdvDataIsConnectable']:
                    # TODO: handle: kCBAdvDataIsConnectable correctly
                    advertisement.type = 0x01 # BLE_GAP_ADV_TYPE_ADV_DIRECT_IND

                if 'kCBAdvDataServiceUUIDs' in data:
                    log.debug('kCBAdvDataServiceUUIDs:')
                    for cbuuid in data['kCBAdvDataServiceUUIDs']:
                        uuid_bytes2 = cbuuid.data().bytes()
                        uuid_bytes = cbuuid.data().bytes().tobytes()
                        log.debug("--------------")
                        log.debug(bytearray_to_hexstring(uuid_bytes))
                        log.debug(bytearray_to_hexstring(uuid_bytes2))

                        if 2 == len(uuid_bytes):
                            uuid = UUID16(uuid_bytes, little_endian=False)
                            advertisement.uuid16s.append(uuid)

                        elif 16 == len(uuid_bytes):
                            uuid = UUID128(uuid_bytes, little_endian=False)
                            advertisement.uuid128s.append(uuid)
                        else:
                            log.error("Unsupporten UUID length for UUID bytes={}".format(uuid_bytes))

                        log.debug('Service UUID: {} {}'.format(type(cbuuid), cbuuid))

                if 'kCBAdvDataManufacturerData' in data:
                    mfg_data=data['kCBAdvDataManufacturerData']
                    log.debug('kCBAdvDataManufacturerData={}'.format(mfg_data))
                    advertisement.mfg_data=mfg_data

                self.on_advertising_data(advertisement)

        except Exception as e:
            log.exception(e)


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
