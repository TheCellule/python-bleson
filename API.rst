Public API
==========

Outline of the 'bleson' Python packages an end-user would use to play with Bluetooth LE.

.. code:: python

    bleson
        get_provider()          # Obtain the Bluetooth LE provider for the current platform (Linux/macOS/Windows)

    bleson.core.types           # Value objects representing Bluetooth Core Spec data types
        BDAddress
        Device
        Advertisement

    bleson.core.roles           # Core Bluetooth roles
        Advertiser
        Observer

    bleson.beacons.eddystone
        EddystoneBeacon         # Physical Web beacon, is a subclass of Advertiser role

    bleson.logger
        log                     # Simple convenience wrapper around Python's standard logging.



Internal API
============


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

