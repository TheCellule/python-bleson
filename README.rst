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

The supported Bluetooth LE roles are: Observer, Advertiser (inc. Beacon), Peripheral* and Central*.

The supported platforms are: Linux (e.g. Raspberry Pi), macOS and Windows 10.

Other highlights:

- The same Bleson API is used across all platforms.
- Only standard platform provided Bluetooth LE API's are used.
- Bleson does not impose a 'mainloop' on user scripts on any platform.
- A compiler is not needed to install Bleson or for updating any system components, in most scenarios.



Status
======

Currently in an early Alpha stage.

Only the Observing and Scanning roles are currently implemented amnd not necessarily fully on each platform, in summary:

Linux:      Observing and Advertising works, it is the most functional of all 3 platforms.

Mac:        Observing and Advertising works, but the actual published Advertisement data is ultimately decided by the OS.

Windows:    Observing works but Advertising used hardcoded test payload data for now.


Documentation
=============

You can find the latest documentation and examples online `here <http://bleson.readthedocs.io/en/latest/>`_.


Install
=======

For platform specifc installation instructions please see the `installtion instructions <http://bleson.readthedocs.io/en/latest/installing.html>`_.

For the impatient, on any supported platform, try this:

.. code::

    pip3 install bleson
    python3 -m bleson --observer

Note: You may need to run 'pip3' with sudo on your platform,

Note: You may need to run 'python' for python3 on your platform. (e.g. Windows)


Feedback
========

All feedback is welcomed and greatly appreciated, please feel free to:

- Post a suggestion or question on the Bleson GoogleGroup_
- Raise a GitHub Issue_
- Submit a PR!

Thanks!



.. _Issue: https://github.com/TheCellule/python-bleson/issues/
.. _GoogleGroup: https://groups.google.com/group/python-bleson/


