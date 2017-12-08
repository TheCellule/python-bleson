python-bleson
=============

.. image:: https://img.shields.io/codecov/c/github/TheCellule/python-bleson/master.svg?maxAge=2592000
    :target: https://codecov.io/github/TheCellule/python-bleson
    :alt: Code Coverage

.. image:: https://img.shields.io/pypi/v/bleson.svg
   :target: https://pypi.python.org/pypi/bleson/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/l/bleson.svg
   :target: https://github.com/TheCellule/python-bleson/blob/master/LICENSE
   :alt: MIT License

Bleson is a cross platform Python 3 module for accessing Bluetooth LE API's.

The (planned) supported Bluetooth LE roles are: Observer, Advertiser (inc. Beacon), Peripheral and Central.

The supported platforms are: Linux (e.g. Raspberry Pi), macOS and Windows 10.

There is also early support for MicroPython running on Noridc's nRF5x devices (e.g. from the micro:bit and up)

Other highlights:

- The same Bleson API is used across all platforms.
- Only standard OS provided Bluetooth LE API's are used.
- Bleson does not impose a 'mainloop' on user scripts on any platform.
- A compiler is not needed to install Bleson or for updating any system components, in most scenarios.



Status
======

Currently in an early Alpha stage.

Only the Observing and Scanning roles are currently implemented and are not necessarily complete on each platform, in summary:

Linux:      Observing and Advertising works, it is the most functional of all 3 platforms.

Mac:        Observing and Advertising works, but the actual published Advertisement data is ultimately decided by the OS.

Windows:    Observing works but Advertising used hardcoded test payload data for now.


Documentation
=============

You can find the latest documentation and examples online `here <http://bleson.readthedocs.io/en/latest/>`_.


Install
=======

For each platform's installation please see these `installation instructions <http://bleson.readthedocs.io/en/latest/installing.html>`_.

For the impatient, try this on any of the supported platforms:

.. code::

    pip3 install bleson
    python3 -m bleson --observer

Note: You may need to run 'pip3' with sudo on your platform, unless you use a virtualenv or `--user` options

Note: You may need to run 'python' for python3 on your platform. (e.g. Windows)


Feedback
========

All feedback is welcomed and greatly appreciated, please feel free to:

- Post a suggestion or question on the Bleson GoogleGroup_
- Raise a GitHub Issue_
- Submit a PR

Thanks!


.. _Issue: https://github.com/TheCellule/python-bleson/issues/
.. _GoogleGroup: https://groups.google.com/group/python-bleson/


