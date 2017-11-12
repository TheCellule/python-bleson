import uuid
import threading
import objc
from PyObjCTools import AppHelper

# https://gist.github.com/jeamland/11284662

objc.loadBundle("CoreBluetooth", globals(),
                bundle_path=objc.pathForFramework(
                    u'/System/Library/Frameworks/IOBluetooth.framework/Versions/A/Frameworks/CoreBluetooth.framework'))


def main():
    delegate = TestCoreBluetoothAdvertisement()
    manager = CBPeripheralManager.alloc()

    # https://developer.apple.com/documentation/corebluetooth/cbperipheralmanager/1393295-init
    manager.initWithDelegate_queue_options_(delegate, None, None)

    try:
        print("starting")
        AppHelper.runConsoleEventLoop(installInterrupt=True)
    except KeyboardInterrupt:
        AppHelper.stopEventLoop()



class TestCoreBluetoothAdvertisement():

    def __init__(self):
        self.manager = None
        self.peripheral = None
        self._connected = threading.Event()

    def peripheralManagerDidUpdateState_(self, manager):
        print("peripheralManagerDidUpdateState_")
        self.manager = manager
        self.start_advertising()

    def start_advertising(self):
        adv_data = {
            'CBAdvertisementDataLocalNameKey': 'bleson',
            #'CBAdvertisementDataServiceUUIDsKey': CBUUID.UUIDWithString_(u'6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
            'CBAdvertisementDataServiceUUIDsKey': CBUUID.UUIDWithString_(u'0xFFEF')
        }
        self.manager.startAdvertising_(adv_data)


    def peripheralManagerDidStartAdvertising_error_(self, peripheral, error):
        print("peripheralManagerDidStartAdvertising_error_ {} {}".format(peripheral, error))


if __name__ == "__main__":
    main()