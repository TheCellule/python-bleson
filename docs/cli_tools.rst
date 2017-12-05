Command-Line tools
******************

Bleson ships with built-in utilities that can be run directly from the command line.

Observer
========

Scan for nearby Bluetooth LE devices and print out any Advertising Reports received:

.. code-block:: console

    $ python3 -m bleson --observer


Beacon
======

Start a PhysicalWeb (Eddystone) beacon advertising a URL:

.. code-block:: console

    $ python3 -m bleson --beacon --url http://www.google.com/

