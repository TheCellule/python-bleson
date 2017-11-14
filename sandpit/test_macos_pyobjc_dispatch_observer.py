import threading
from logging import getLogger, basicConfig, DEBUG
from time import sleep
import objc
from Foundation import *
from PyObjCTools import AppHelper
import CoreBluetooth

from ctypes import cdll, Structure, POINTER, pointer, c_int, c_char_p, c_void_p, cast
# http://python.net/crew/theller/ctypes/tutorial.html

#from objc import se
#objc.setObjCPointerIsError(True)

OpaqueType = objc.createOpaquePointerType("OpaqueType", b"^{OpaqueType}", None)


basicConfig(level=DEBUG, format='%(asctime)s %(levelname)6s - %(funcName)24s(): %(message)s')
log = getLogger(__name__)

USE_BACKGROUND_THREAD = True       # When false OK, when true no CoreBluetooth events
USE_DISPATCH_QUEUE = True          # When false OK, when true SIG


NULL_PTR = POINTER(c_int)()

# Opaque structure that can be used to pass areound 'dispatch_queue_t' C type in a type-safe way
# see: https://stackoverflow.com/questions/5030730/is-it-acceptable-to-subclass-c-void-p-in-ctypes
class dispatch_queue_t(Structure):
    pass


# Load the dispatch library
_lib = cdll.LoadLibrary("/usr/lib/system/libdispatch.dylib")

_dispatch_queue_create = _lib.dispatch_queue_create
_dispatch_queue_create.argtypes = [c_char_p, c_void_p]
#_dispatch_queue_create.restype = POINTER(dispatch_queue_t)
_dispatch_queue_create.restype = c_void_p

def dispatch_queue_create(name):
    # https://developer.apple.com/documentation/dispatch/1453030-dispatch_queue_create
    b_name = name.encode('utf-8')
    c_name = c_char_p(b_name)
    queue = _dispatch_queue_create(c_name, NULL_PTR)

    return queue


class TestCoreBluetooth():

    def __init__(self):
        self._manager = None
        self._dispatch_queue = dispatch_queue_create('myq') if USE_DISPATCH_QUEUE else None


    def start(self):
        if USE_BACKGROUND_THREAD:
            self._socket_poll_thread = threading.Thread(target=self._runloop, name='mythread')
            self._socket_poll_thread.setDaemon(True)
            self._socket_poll_thread.start()
        else:
            self._runloop()


    # https://pythonhosted.org/pyobjc/core/intro.html#working-with-threads
    def _runloop(self):
        log.info("")
        try:
            pool = NSAutoreleasePool.alloc().init()

            self._manager = CoreBluetooth.CBCentralManager.alloc()

            # queue_ptr = self._dispatch_queue      # the ctypes object of dispatch_queue_t* returned from dispatch_queue_create()
            # queue_ptr = OpaqueType(c_void_p=self._dispatch_queue)
            queue_ptr = objc.objc_object(c_void_p=self._dispatch_queue)
            self._manager.initWithDelegate_queue_options_(self, queue_ptr, None)

            log.info('Starting RunLoop, dispatch_queue={}'.format(self._dispatch_queue))
            rc = AppHelper.runConsoleEventLoop(installInterrupt=True)
            log.info("RC=",rc)
        except Exception as e:
            log.exception(e)
        finally:
            AppHelper.stopEventLoop()
            if pool:
                del pool
        log.info("Ending")


    # CoreBluetooth Protocol

    def centralManagerDidUpdateState_(self, manager):
        log.info("")
        self._manager.scanForPeripheralsWithServices_options_(None, None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        log.info('Found: name={} rssi={} data={} '.format(peripheral.name(), rssi, data))

    def centralManager_didConnectPeripheral_(self, manager, peripheral):
        log.info("")

    def centralManager_didFailToConnectPeripheral_error_(self, manager, peripheral, error):
        log.error(repr(error))

    def centralManager_didDisconnectPeripheral_error_(self, manager, peripheral, error):
        log.info("")

    def peripheral_didDiscoverServices_(self, peripheral, error):
        log.info("")

    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
        log.info("")

    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        log.info("")

    def peripheral_didUpdateNotificationStateForCharacteristic_error_(self, peripheral, characteristic, error):
        log.info("peripheral_didUpdateNotificationStateForCharacteristic_error_")


    def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
        log.error(repr(error))


if __name__ == "__main__":
    bt = TestCoreBluetooth()
    bt.start()
    sleep(10)