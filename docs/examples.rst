Examples
********

Observer example
----------------

Scan for local devices.

    .. testcode:: Observer

       from time import sleep
       from bleson import get_provider, Observer

       def on_advertisement(advertisement):
          print(advertisement)

       adapter = get_provider().get_adapter()

       observer = Observer(adapter)
       observer.on_advertising_data = on_advertisement

       observer.start()
       sleep(2)
       observer.stop()

    This will output one or more lines containing an AdvertisingReport for each Bluetooth LE device found, for example:

    .. testoutput:: Observer

       Advertisement(...)


Advertiser example
------------------

Advertise the host as a Bluetooth LE device with the name `bleson`

    .. testcode:: Advertiser

       from time import sleep
       from bleson import get_default_adapter, Advertiser, Advertisement

       adapter = get_default_adapter()

       advertiser = Advertiser(adapter)
       advertisement = Advertisement()
       advertisement.name = "bleson"

       advertiser.advertisement = advertisement

       advertiser.start()
       sleep(2)
       advertiser.stop()



PhysicalWeb beacon example
--------------------------

Create a PhysicalWeb (Eddystone) with a URL

    .. testcode:: Beacon

        from time import sleep
        from bleson import get_provider, EddystoneBeacon

        adapter = get_provider().get_adapter()

        beacon = EddystoneBeacon(adapter)
        beacon.url = 'https://www.bluetooth.com/'
        beacon.start()
        sleep(2)
        beacon .stop()



Further Reading
---------------

Please see examples_ for more details.

+ Examples prefixed with 'basic' shows basic Bleson API usage.
+ Examples prefixed with 'context' shows Blesons context manger ('with' keyword) API usage.

.. _examples: https://github.com/TheCellule/python-bleson/tree/master/examples/

