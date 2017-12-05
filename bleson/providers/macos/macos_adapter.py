from threading import Thread, Event, Lock
import ctypes

from bleson.interfaces.adapter import Adapter
from bleson.core.types import Advertisement, UUID16, UUID128
from bleson.core.hci.constants import *
from bleson.logger import log
from bleson.core.hci.type_converters import bytearray_to_hexstring

# Work around for Sphinx
try:
    import objc
    from Foundation import *
    from PyObjCTools import AppHelper
    import CoreBluetooth
except (ImportError, AttributeError) as e:
    import sys
    if 'sphinx' in sys.modules:
        log.warning("macOS modules not found, if this is a documentation build all is good")
    else:
        log.error("macOS modules not found, but this doesn't look like a documentation build")
        raise e


######################################
# Dispatch Queue support

# see: https://bitbucket.org/ronaldoussoren/pyobjc/issues/215/starting-runconsoleeventloop-from-a

# Opaque structure use to pass areound 'dispatch_queue_t' C type
# see: https://stackoverflow.com/questions/5030730/is-it-acceptable-to-subclass-c-void-p-in-ctypes
#class dispatch_queue_t(ctypes.Structure):
#    pass
# The above is not used as the PyObcC 4.0.1 doesn't accept it as a type to create the pointer to the dispatch_queu_

NULL_PTR = ctypes.POINTER(ctypes.c_int)()
_lib = None

# lazy load the library, helps Sphinx.
def dispatch_queue_create(name):
    global _lib, _dispatch_queue_create
    if not _lib:
        # Load the dispatch library, once
        _lib = ctypes.cdll.LoadLibrary("/usr/lib/system/libdispatch.dylib")

    _dispatch_queue_create = _lib.dispatch_queue_create
    _dispatch_queue_create.argtypes = [ctypes.c_char_p, ctypes.c_void_p]  # 2nd param is stuct, but we don't use it.
    _dispatch_queue_create.restype = ctypes.c_void_p
    # https://developer.apple.com/documentation/dispatch/1453030-dispatch_queue_create

    b_name = name.encode('utf-8')
    c_name = ctypes.c_char_p(b_name)
    return _dispatch_queue_create(c_name, NULL_PTR)


# The adapter is a singleton because of the (singleton) nature of the underlying native NSApp runtime.
class Singleton(type):
    _instances = {}
    __singleton_lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls.__singleton_lock:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CoreBluetoothAdapter(Adapter, metaclass=Singleton):

    # states
    poweredOn = 5

    def __init__(self, device_id=0):
        self.device_id = device_id
        self.on_advertising_data = None
        self.connected = False
        self._keep_running = True
        self._socket_poll_thread = Thread(target=self._runloop_thread, name='BlesonObjCRunLoop')
        self._socket_poll_thread.setDaemon(True)
        self._dispatch_queue = dispatch_queue_create('blesonq')
        self._manager = None
        self._peripheral_manager = None
        self._runloop_started_lock = Event()

        self._socket_poll_thread.start()

    def open(self):
        self.wait_for_event_timeout(self._runloop_started_lock)
        #self._runloop_started_lock.set()

    def on(self):
        log.debug("TODO: adatper on")

    def off(self):
        log.debug("TODO: adatper off")

    def wait_for_event_timeout(self, e, t=5):
        while not e.isSet():
            log.debug('wait_for_event_timeout starting')
            event_is_set = e.wait(t)
            log.debug('event set: %s', event_is_set)


    def start_scanning(self):
        self.wait_for_event_timeout(self._runloop_started_lock)
        if self._manager:
            self._manager.scanForPeripheralsWithServices_options_(None, None)

    def stop_scanning(self):
        log.debug("")
        if self._manager:
            self._manager.stopScan()


    def start_advertising(self, advertisement, scan_response=None):
        log.warning("TODO")
        return
        adv_data = {
            'CBAdvertisementDataLocalNameKey': 'bleson',
            #'CBAdvertisementDataServiceUUIDsKey': CBUUID.UUIDWithString_(u'6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
            'CBAdvertisementDataServiceUUIDsKey': CBUUID.UUIDWithString_(u'0xFFEF')
        }
        self._peripheral_manager.startAdvertising_(adv_data)

    def stop_advertising(self):
        log.warning("TODO")
        return
        adv_data = {
            'CBAdvertisementDataLocalNameKey': 'bleson',
            #'CBAdvertisementDataServiceUUIDsKey': CBUUID.UUIDWithString_(u'6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
            'CBAdvertisementDataServiceUUIDsKey': CBUUID.UUIDWithString_(u'0xFFEF')
        }
        if self._peripheral_manager.isAdvertising:
            self._peripheral_manager.stopAdvertising()




    # https://pythonhosted.org/pyobjc/core/intro.html#working-with-threads
    def _runloop_thread(self):
        try:
            with objc.autorelease_pool():
                queue_ptr = objc.objc_object(c_void_p=self._dispatch_queue)

                self._manager = CoreBluetooth.CBCentralManager.alloc()
                self._manager.initWithDelegate_queue_options_(self, queue_ptr, None)

                #self._peripheral_manager = CoreBluetooth.CBPeripheralManager.alloc()
                #self._peripheral_manager.initWithDelegate_queue_options_(self, queue_ptr, None)
                self._runloop_started_lock.set()
                AppHelper.runConsoleEventLoop(installInterrupt=True)
        except Exception as e:
            log.exception(e)
        log.info("Exiting runloop")


    # CoreBluetooth PeripheralManager Protocol

    def peripheralManagerDidUpdateState_(self, manager):
        state = manager.state()
        log.debug("State: {}".format(state))

    def peripheralManagerDidStartAdvertising_error_(self, peripheral, error):
        print("peripheralManagerDidStartAdvertising_error_ {} {}".format(peripheral, error))


    # CoreBluetooth CentralManager Protocol

    def centralManagerDidUpdateState_(self, manager):
        state = manager.state()
        log.debug("State: {}".format(state))


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
        #AppHelper.stopEventLoop()

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
