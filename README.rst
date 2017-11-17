=============
python-bleson
=============

Bleson is a cross platform Python 3 module for using Bluetooth LE.

Supported Bluetooth LE roles are: Observer, Advertiser, Peripheral and Central.

The supported platforms are Linux, macOS and Windows 10.

A compiler is not needed to install Bleson and for each platform only the standard built-in OS API's are used.

Status
======

Currently an Alpha release, all areas are WIP and subject to change.

Only the Observing and Scanning roles are currently implemented, not necessarily fully on each platform, in summary:

Linux:      Observing and Advertising works, it is the most functional of all 3 platforms.

Mac:        Observing and Advertising works, but the actual published Advertisement data is managed by the OS.

Windows:    Observing works but starting Advertising will result in a crash.


Feedback
========

All feedback is welcomed and greatly appreciated, please feel free to:

- Post a suggestion or question on the Bleson GoogleGroup_
- Raise a GitHub Issue_.

Thanks!


Quick Test
==========

For the impatient, try this:

```python
pip3 install bleson
python3 -m bleson --observer
```

You may need to run 'pip3' with sudo on your platform,
You may need to run 'python' for python3 on your platform. (Windows)

Install
=======

```python
pip3 install bleson
```

You may need to run 'pip3' with sudo on your platform.

Running - Linux
===============

User Python scripts will need to run as root, see the 'Rootless Linux' section below to remove this constraint.

It's currently not necessary to stop the bluetoothd service for observing, but because Bleson uses the HCI socket interface directly, it is recommended.

For example, to do on a Raspberry Pi:
```bash
sudo service bluetooth stop
```

Running - macOS
===============

On Mac the system bundled Python is version 2, you will need Python 3 from Python_.


Running - Windows
=================

You need to be running at least Windows 10 Fall Creators Update (build 16299, 64bit)

The 'blesonwin' binary package has only been built and tested with Python 3.6.32.



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


Examples
========

Please see examples_ for more details.
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

Please see the tests_ folder.




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

.. _Python: http://www.python.org/
.. _Issues: https://github.com/TheCellule/python-bleson/issues
.. _Install: https://pythonhosted.org/pyobjc/install.html
.. _GoogleGroup: https://groups.google.com/group/python-bleson