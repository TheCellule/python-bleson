import time
import struct
from threading import Timer
import objc
from PyObjCTools import AppHelper

# install:  https://www.python.org/downloads/release/python-363/
# pip3 install obcj

# see: https://github.com/ppossemiers/BLECrazyflie_Python/blob/master/ble_crazyflie.py


objc.loadBundle("CoreBluetooth", globals(),
                bundle_path=objc.pathForFramework(
                    u'/System/Library/Frameworks/IOBluetooth.framework/Versions/A/Frameworks/CoreBluetooth.framework'))

#dfu_service = CBUUID.UUIDWithString_(u'00001530-1212-efde-1523-785feabcd123')
#dfu_characteristic = CBUUID.UUIDWithString_(u'00001531-1212-efde-1523-785feabcd123')
crazyflie_service = CBUUID.UUIDWithString_(u'6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
crtp_characteristic = CBUUID.UUIDWithString_(u'6E400002-B5A3-F393-E0A9-E50E24DCCA9E')  # TX char

print(crazyflie_service)

def main():
    # Ctrl + \ kills the script on MacOS
    cf = BLECrazyFlie()
    # add methods that the crazyflie executes
    cf.add_callback(hover)
    manager = CBCentralManager.alloc()
    manager.initWithDelegate_queue_options_(cf, None, None)

    try:
        print("starting")
        AppHelper.runConsoleEventLoop(installInterrupt=True)
    except KeyboardInterrupt:
        AppHelper.stopEventLoop()


def hover(cf):
    print('hover')
    # take off
    for i in range(2):
        cf.send_setpoint(0, 0, 0, 50000)
        time.sleep(0.5)

    # stop thrust, start hover
    cf.set_param(11, 'b', 1)
    cf.send_setpoint(0, 0, 0, 32767)
    while 1:
        cf.send_setpoint(0, 0, 0, 32767)
        time.sleep(0.5)


class BLECrazyFlie():
    def __init__(self):
        self.manager = None
        self.peripheral = None
        self.service = None
        self.crtp_characteristic = None
        self.connected = False
        self.callbacks = []

        self.init = False

    def send_setpoint(self, roll, pitch, yaw, thrust):
        data = struct.pack('<BfffH', 0x30, roll, -pitch, yaw, thrust)
        bytes = NSData.dataWithBytes_length_(data, len(data))
        self.peripheral.writeValue_forCharacteristic_type_(bytes, self.crtp_characteristic, 1)

    def add_callback(self, cb):
        if ((cb in self.callbacks) is False):
            self.callbacks.append(cb)

    def remove_callback(self, cb):
        self.callbacks.remove(cb)

    def call(self, *args):
        print("call")
        for cb in self.callbacks:
            cb(*args)

    def centralManagerDidUpdateState_(self, manager):
        print("centralManagerDidUpdateState_")

        if self.connected == False:
            self.manager = manager
            manager.scanForPeripheralsWithServices_options_(None, None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        print("centralManager_didDiscoverPeripheral_advertisementData_RSSI_")
        print('Found: name={} rssi={} data={} '.format(peripheral.name(), rssi, data))

        if peripheral.name() == 'Crazyflie':
            manager.stopScan()
            self.peripheral = peripheral
            manager.connectPeripheral_options_(self.peripheral, None)


    def centralManager_didConnectPeripheral_(self, manager, peripheral):
        print("centralManager_didConnectPeripheral_")

        print('Conencted: ' + peripheral.name())
        self.connected = True
        self.peripheral.setDelegate_(self)
        self.peripheral.readRSSI()
        self.peripheral.discoverServices_([crazyflie_service])

    def centralManager_didFailToConnectPeripheral_error_(self, manager, peripheral, error):
        print("centralManager_didFailToConnectPeripheral_error_")

        print(repr(error))

    def centralManager_didDisconnectPeripheral_error_(self, manager, peripheral, error):
        print("centralManager_didDisconnectPeripheral_error_")
        self.connected = False
        AppHelper.stopEventLoop()

    def peripheral_didDiscoverServices_(self, peripheral, error):
        print("peripheral_didDiscoverServices_")
        if (error == None):
            self.service = self.peripheral.services()[0]
            self.peripheral.discoverCharacteristics_forService_([crtp_characteristic], self.service)

    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
        print("peripheral_didDiscoverCharacteristicsForService_error_")

        for characteristic in self.service.characteristics():
            if characteristic.UUID().UUIDString() == crtp_characteristic.UUIDString():
                self.crtp_characteristic = characteristic
                self.peripheral.setNotifyValue_forCharacteristic_(True, self.crtp_characteristic)

    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print("peripheral_didWriteValueForCharacteristic_error_")

        if error != None:
            print(repr(error))

    def peripheral_didUpdateNotificationStateForCharacteristic_error_(self, peripheral, characteristic, error):
        print("peripheral_didUpdateNotificationStateForCharacteristic_error_")

        print('Receiving notifications')
        # unlock thrust
        self.send_setpoint(0, 0, 0, 0)
        self.call(self)

    def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print("peripheral_didUpdateValueForCharacteristic_error_")

        print('Updated value')
        repr(characteristic.value().bytes().tobytes())

    def set_param(self, ident, pytype, value):
        print("set_param")

        PARAM = 0x02
        WRITE_CHANNEL = 2
        header = ((0x02 & 0x0f) << 4 | 3 << 2 | (2 & 0x03))
        format = '<BB' + pytype
        data = struct.pack(format, header, ident, value)
        print(struct.unpack(format, data))
        bytes = NSData.dataWithBytes_length_(data, len(data))
        self.peripheral.writeValue_forCharacteristic_type_(bytes, self.crtp_characteristic, 1)


if __name__ == "__main__":
    main()