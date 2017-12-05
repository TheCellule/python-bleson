Internal API
============

Needs to be extended to support GATT etc.

API - Linux
-----------

Bleson uses the HCI Sockets interface, so is not dependat on the userland BlueZ componenets, it's pure Python sockets.

API - Mac
---------

The CoreBluetooth dispatch queue is run in a background thread, requires the use of features added in PyObjC 4.1 for macOS < 10.12.


API - Windows
-------------

On Windows there is a additional module used called 'blesonwin', it provides a native Python module to access the WinRT BLE API's.
It's not recommended to use this module directly in user scripts.

