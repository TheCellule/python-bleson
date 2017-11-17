=============
python-bleson
=============

Bleson is a cross platform Python 3 module for using Bluetooth LE.

Platforms supported are : Linux, macOS & Windows 10.

Supported Bluetooth LE roles are: Observer, Advertiser, Peripheral and Central.

Bleson is intended to have minimal dependencies and can be installed using just 'pip' on all platforms.



Status
======

Currently an Alpha release, all areas are WIP and subject to change.

Only Observing and Scanning API's are currently implemented, not necessarily fully on each platform.

Linux:      Observing and Advertising works, it is the most functional of all 3 platforms.

Mac:        Observing and Advertising works, but the actual published Advertisement data is managed by the OS.

Windows:    Observing works but starting Advertising will result in a crash.


Feedback
========

Any and all feedback is greatly appreciated, please feel free to:

- Post a suggestion or question on the [Bleson Google Group](https://groups.google.com/group/python-bleson).
- Raise a [GitHub issue](https://github.com/TheCellule/python-bleson/issues).

Thanks!


Install
=======

Linux
-----

On Linux Bleson uses the HCI Socket interface; the only system BLE dependency is the BlueZ kernel driver, the userland Bluez bluetoothd service can (and for some roles should) be stopped, e.g. there is no need to recompile Bluez from source.

User Python scripts will need to run as root, see the 'Rootless Linux' section below to remove this constraint.

```python
sudo pip3 install bleson
```

It's currently not necessary to stop the bluetoothd service for observing, but it is recommended.

e.g. on a Raspberry Pi:
```bash
sudo service bluetooth stop
```

Mac
---

On Mac the PyObjC module is required, the macOS bundled Python is only version 2, you will need Python 3 and PyObjC.

Assuming you have installed Python3 using Homebrew (which doesn't require sudo to update) run:

```python
pip3 install bleson pyobjc
```


Windows
-------

You need to be running at least Windows 10 Fall Creators Update (build 16299, 64bit)

On Windows there is a additional module called 'blesonwin' which provides a native Python module to access the WinRT BLE API's.

The 'blesonwin' binary package has only been built and tested with Python 3.6.32.

```python
pip install bleson blesonwin
```


Touch test
==========

To check the library is functioning ok run the following to find nearby Bluetooth LE devices :

```python
python3 -m bleson --observer
```

You should see lines of the form:

```bash
Advertisement(flags=0x06, name=b'BBC micro:bit [tegip]', rssi=-86)
```

You may also see other debug output and warnings.


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



Examples
========

Please see [examples](examples) for more details.
Examples prefixed with 'basic_' shows basic Bleson API usage.
Examples prefixed with 'context_' shows Blesons context maanger ('with' keyword) API usage.


Example - Advertiser
--------------------

Shows how to create custom advertisement.

Example - Eddystone Beacon
--------------------------

Shows how to setup a Physical Web beacon

Example - Observer
------------------

Shows how to scan for local devices.


Tests
=====

Please see the [tests](tests) folder.



Rootless Linux
==============

To run without using root you can use the `setcap` utility to give the Python3 binary permission, for example:

Raspberry Pi Jessie

```bash
sudo setcap cap_net_raw+eip $(eval readlink -f `which python3`)
```

Raspberry Pi Stretch

```bash
sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)
```

