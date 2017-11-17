Public API
==========

Outline of the 'bleson' Python packages an end-user would use to play with Bluetooth LE.

.. code:: python

    bleson
        get_provider()          # Obtain the Bluetooth LE provider for the current platform (Linux/macOS/Windows)

    bleson.core.types           # Value objects representing Bluetooth Core Spec data types
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

