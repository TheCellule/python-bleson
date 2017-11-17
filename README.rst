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

Please see 'examples' folder for more details.
Examples prefixed with 'basic_' shows basic Bleson API usage.
Examples prefixed with 'context_' shows Blesons context maanger ('with' keyword) API usage.


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

Please see the 'tests' folder.


Internal API
============

To be continued...

