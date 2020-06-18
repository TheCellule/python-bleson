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

    from bleson import get_provider, Advertiser, Advertisement

    adapter = get_provider().get_adapter()

    advertiser = Advertiser(adapter)
    advertisement = Advertisement()
    advertisement.name = "bleson"

    advertiser.advertisement = advertisement

    advertiser.start()
    sleep(10)
    advertiser.stop()

Peripheral example
------------------

Create a simple Peripheral

    .. testcode:: Peripheral_LED

        from time import sleep
        from bleson import get_default_adapter, Peripheral, Service, Characteristic, CHAR_WRITE

        adapter = get_default_adapter()

        peripheral = Peripheral(adapter)

        MICROBIT_LED_SERVICE = 'E95DD91D-251D-470A-A062-FA1922DFA9A8'
        MICROBIT_LED_CHAR = 'E95D7B77-251D-470A-A062-FA1922DFA9A8'

        def on_data_received(bytes):
            print(bytes)

        led_service = Service(MICROBIT_LED_SERVICE)
        led_write_char = Characteristic(MICROBIT_LED_CHAR, CHAR_WRITE)
        led_write_char.on_data_received = on_data_received

        led_service.add_characteristic(led_write_char)

        peripheral.add_service(led_service)

        peripheral.start()
        sleep(2)
        peripheral.stop()



PhysicalWeb beacon example
--------------------------

Create a PhysicalWeb (Eddystone) with a URL

    .. testcode:: Beacon

        from time import sleep
        from bleson import get_default_adapter, EddystoneBeacon

        adapter = get_default_adapter()

        beacon = EddystoneBeacon(adapter)
        beacon.url = 'https://www.bluetooth.com/'
        beacon.start()
        sleep(2)
        beacon.stop()



Further Reading
---------------

Please see examples_ for more details.

+ Examples prefixed with 'basic' shows basic Bleson API usage.
+ Examples prefixed with 'context' shows Blesons context manger ('with' keyword) API usage.

.. _examples: https://github.com/TheCellule/python-bleson/tree/master/examples/

