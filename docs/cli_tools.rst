CLI tools
**********

Bleson ships with built-in utilities that can be from the command line shell.

Observer
========

Scan for nearby Bluetooth LE devices and print out any Advertising Reports found:

.. code-block:: console

    $ python3 -m bleson --observer


Beacon
======

Start a PhysicalWeb (Eddystone) beacon advertising a URL:

.. code-block:: console

    $ python3 -m bleson --beacon --url http://www.google.com/

