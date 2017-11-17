python-bleson
=============

.. image:: https://img.shields.io/codecov/c/github/TheCellule/python-bleson/master.svg?maxAge=2592000
    :target: https://codecov.io/github/TheCellule/python-bleson
    :alt: Code Coverage

.. image:: https://img.shields.io/pypi/v/bluezero.svg
   :target: https://pypi.python.org/pypi/bleson/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/l/bluezero.svg
   :target: https://github.com/TheCellule/python-bleson/blob/master/LICENSE
   :alt: MIT License

Bleson is a cross platform Python 3 module for using Bluetooth LE.

The supported Bluetooth LE roles are: Observer, Advertiser (inc. Beacon), Peripheral* and Central*.

The supported platforms are: Linux, macOS and Windows 10.

Other highlights:

- The same Bleson API is used across all supported platforms.
- Only the standard built-in OS provided Bluetooth LE API's are used on each platform.
- Bleson does not impose a 'mainloop' on user scripts on any platform.
- A compiler is not needed to install Bleson or for updating any system components.

Status
======

Currently in an early Alpha stage.

Only the Observing and Scanning roles are currently implemented amnd not necessarily fully on each platform, in summary:

Linux:      Observing and Advertising works, it is the most functional of all 3 platforms.

Mac:        Observing and Advertising works, but the actual published Advertisement data is ultimately decided by the OS.

Windows:    Observing works but starting Advertising will result in a crash.


Feedback
========

All feedback is welcomed and greatly appreciated, please feel free to:

- Post a suggestion or question on the Bleson GoogleGroup_
- Raise a GitHub Issue_
- Submit a PR!

Thanks!


Quick Test
==========

For the impatient, try this:

.. code::

    pip3 install bleson
    python3 -m bleson --observer

You may need to run 'pip3' with sudo on your platform,
You may need to run 'python' for python3 on your platform. (Windows)

Install
=======

.. code:: bash

    pip3 install bleson

You may need to run 'pip3' with sudo on your platform.

As Python package management seems to be going thru a bit of a change probably a good idea to update :

.. code::

    pip3 install --upgrade pip setuptools wheel twine



Running - Linux
===============

User Python scripts will need to run as root, see the 'Rootless Linux' section below to remove this constraint.

It's currently not necessary to stop the bluetoothd service for observing, but because Bleson uses the HCI socket interface directly, it is recommended.

For example, to do on a Raspberry Pi:

.. code:: bash

    sudo service bluetooth stop

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

.. code:: bash

    python3 -m bleson --observer

You should see lines of the form:

.. code:: python

    Advertisement(flags=0x06, name=b'BBC micro:bit [tegip]', rssi=-86)


You may also see other debug output and warnings during this Alpha stage of development.


Examples
========

Please see examples_ for more details.
Examples prefixed with 'basic' shows basic Bleson API usage.
Examples prefixed with 'context' shows Blesons context maanger ('with' keyword) API usage.


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

.. code:: bash

    sudo setcap cap_net_raw+eip $(eval readlink -f `which python3`)

Raspberry Pi Stretch

.. code:: bash

    sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)


.. _Python: https://www.python.org/downloads/
.. _Issue: https://github.com/TheCellule/python-bleson/issues/
.. _GoogleGroup: https://groups.google.com/group/python-bleson/
.. _examples: https://github.com/TheCellule/python-bleson/tree/master/examples/
.. _tests: https://github.com/TheCellule/python-bleson/tree/master/tests/
