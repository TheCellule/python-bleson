Internal API
************

Abstract Interfaces
===================

.. autoclass:: bleson.interfaces.provider.Provider
    :members:

.. autoclass:: bleson.interfaces.adapter.Adapter
    :members:

.. autoclass:: bleson.interfaces.role.Role
    :members:

.. autoclass:: bleson.core.types.ValueObject
    :members:

    .. automethod:: __bytes__
    .. automethod:: __len__



Platform Implementations
========================

Linux
-----

Bleson uses the Linux kernel's HCI Sockets interface, is not dependent on the userland BlueZ service or binaries, it's pure Python sockets.

.. autoclass:: bleson.providers.linux.linux_provider.LinuxProvider
   :members:

.. autoclass:: bleson.providers.linux.linux_adapter.BluetoothHCIAdapter
   :members:


macOS
-----

The CoreBluetooth dispatch queue is run in a background thread, requires the use of features added in PyObjC 4.1 for macOS < 10.12.

.. autoclass:: bleson.providers.macos.macos_provider.MacOSProvider
   :members:

.. autoclass:: bleson.providers.macos.macos_adapter.CoreBluetoothAdapter
   :members:

Windows
-------

On Windows there is an additional module used called 'blesonwin', it provides a Python native module to access the WinRT BLE API's.
It's not recommended to use this module directly in user scripts.


.. autoclass:: bleson.providers.win32.win32_provider.Win32Provider
   :members:

.. autoclass:: bleson.providers.win32.win32_adapter.BluetoothAdapter
   :members:

