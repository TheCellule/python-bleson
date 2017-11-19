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
import ctypes


######################################
# Dispatch Queue support

# see: https://bitbucket.org/ronaldoussoren/pyobjc/issues/215/starting-runconsoleeventloop-from-a

# Opaque structure use to pass areound 'dispatch_queue_t' C type
# see: https://stackoverflow.com/questions/5030730/is-it-acceptable-to-subclass-c-void-p-in-ctypes
#class dispatch_queue_t(ctypes.Structure):
#    pass
# The above is not used as the PyObcC doest accept it as a type to create the pointer to the dispatch_queu_

NULL_PTR = ctypes.POINTER(ctypes.c_int)()


# Load the dispatch library
_lib = ctypes.cdll.LoadLibrary("/usr/lib/system/libdispatch.dylib")

_dispatch_queue_create = _lib.dispatch_queue_create
_dispatch_queue_create.argtypes = [ctypes.c_char_p, ctypes.c_void_p]  # 2nd param is stuct, but we don't use it.
_dispatch_queue_create.restype = ctypes.c_void_p
# https://developer.apple.com/documentation/dispatch/1453030-dispatch_queue_create



def dispatch_queue_create(name):
    b_name = name.encode('utf-8')
    c_name = ctypes.c_char_p(b_name)
    return _dispatch_queue_create(c_name, NULL_PTR)


class CoreBluetoothAdapter(Adapter):

    def __init__(self, device_id=0):
        self.device_id = device_id
        self.connected = False
        self._keep_running = True
        self._socket_poll_thread = threading.Thread(target=self._runloop_thread, name='BlesonObjCRunLoop')
        self._socket_poll_thread.setDaemon(True)
        self._dispatch_queue = dispatch_queue_create('blesonq')
        self._manager = CoreBluetooth.CBCentralManager.alloc()


    def open(self):
        pass


    def on(self):
        log.debug("TODO: adatper on")

    def off(self):
        log.debug("TODO: adatper off")

    def start_scanning(self):
        self._socket_poll_thread.start()


    def stop_scanning(self):
        AppHelper.stopEventLoop()

    def start_advertising(self, advertisement, scan_response=None):
        raise NotImplementedError

    def stop_advertising(self):
        raise NotImplementedError


    # https://pythonhosted.org/pyobjc/core/intro.html#working-with-threads
    def _runloop_thread(self):
        try:
            with objc.autorelease_pool():
                queue_ptr = objc.objc_object(c_void_p=self._dispatch_queue)
                self._manager.initWithDelegate_queue_options_(self, queue_ptr, None)
                AppHelper.runConsoleEventLoop(installInterrupt=True)
        except Exception as e:
            log.exception(e)
        finally:
            AppHelper.stopEventLoop()

    # CoreBluetooth Protocol

    def centralManagerDidUpdateState_(self, manager):
        log.debug("centralManagerDidUpdateState_")

        if self.connected == False:
            self._manager.scanForPeripheralsWithServices_options_(None, None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        try:
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
                        uuid_bytes = cbuuid.data().bytes().tobytes()

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
        log.debug('Connected: ' + peripheral.name())
        self.connected = True
        self.peripheral.setDelegate_(self)
        self.peripheral.readRSSI()
        #self.peripheral.discoverServices_([CBUUID(...)])

    def centralManager_didFailToConnectPeripheral_error_(self, manager, peripheral, error):
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
        log.debug(repr(characteristic.value().bytes().tobytes()))
