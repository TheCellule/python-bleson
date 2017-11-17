Internal API
============

Needs to be extended to support GATT etc.

API - Linux
-----------

Bleson uses the HCI Sockets interface, so is not dependat on the userland BlueZ componenets, it's pure Python sockets.

API - Mac
---------

To use CoreBluetooth in a background thread Bleson mixes the use of `ctypes` and PyObjC.
A `dispatch_queue_t` is created using `ctypes` and is then passed to the CoreBluetooth managers via PyObjC.


API - Windows
-------------

On Windows there is a additional module used called 'blesonwin', it provides a native Python module to access the WinRT BLE API's.
It's not recommended to use this module directly in user scripts.

