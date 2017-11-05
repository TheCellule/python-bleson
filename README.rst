=============
python-bleson
=============

Status
======

Experimental.


Public API
==========

Outline of the 'bleson' Python packages an end-user would use to play with Bluetooth LE.

.. code:: python

    bleson
        get_provider()          # Obtain the provider for the current platfrom (currently Linux HCI only)

    bleson.core.types           # Value objects representing Bluetooth Core Spec data types (not HCI specific)
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

Examples are abbreviated below, plese see 'examples' folder for more details.

Example - Advertiser
--------------------

.. code:: python

    from bleson import get_provider, Advertiser, Advertisement

    adapter = get_provider().get_adapter()
    advertiser = Advertiser(adapter)
    advertisement = Advertisement(name = "bleson")
    advertiser.start()
    advertiser.stop()


Example - Eddystone Beacon
--------------------------

.. code:: python

    from bleson import get_provider, EddystoneBeacon

    adapter = get_provider().get_adapter()
    beacon = EddystoneBeacon(adapter)
    beacon.url = 'https://www.bluetooth.com/'
    beacons.start()
    beacons.stop()


Example - Observer
------------------

.. code:: python

    from bleson import get_provider, Observer

    adapter = get_provider().get_adapter()

    def on_advertisement(advertisement):
        print(advertisement)

    observer = Observer(adapter)
    observer.on_advertising_data = on_advertisement
    observer.start()
    observer.stop()

Tests
=====

Please see the testsuite in the 'tests' folder.


Internal API
============

To be continued...

