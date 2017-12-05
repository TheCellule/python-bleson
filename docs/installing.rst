Installing
**********

Bleson is currently only compatible with Python 3.


Linux
=====

.. code-block:: console

    $ sudo pip3 install bleson




.. note::

    To run scripts without having to run as root to acced the Bluetooth LE adapter you can use the `setcap` utility to give the Python3 binary necessary permission, for example:

    .. code-block:: console

       sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)


.. note::

    It's currently not necessary to stop the bluetoothd service for observing, but because Bleson uses the HCI socket interface directly, it is recommended.

    For example, on a Raspberry Pi run:

    .. code:: bash

        sudo service bluetooth stop


macOS
=====

.. code-block:: console

    $ pip3 install bleson

You may have to use sudo if you are not using `homebrew`.

.. note::

    On Mac the system bundled Python is version 2, you will need Python 3 from Python_.


.. note::

    Currently only macOS 10.12+ is supported, soon to be resolved (and support macOS 10.9+) when PyObjC 4.1 is released.


Windows 10
==========

.. code-block:: console

    $ pip install bleson


.. note::

    Only Windows 10 Fall Creators Update (build 16299) has been tested and known to work.

    Earlier version of Windows are not supported, and are unlikely to ever be.

.. note::
    You must use pip v9.0 or newer to be able to install bleson's precompiled native components ('wheels') on Mac and Windows.*

.. note::

    The bleson module depends on an native module, `blesonwin`, it will be automatically installed.
    The 'blesonwin' binary (wheel) pacakges have been pre-built for 32bit and 64bit architectures for Python 3.5 and Python 3.6


.. _Python: https://www.python.org/downloads/
