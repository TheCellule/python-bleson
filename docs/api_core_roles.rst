API - Core Bluetooth LE Roles
*****************************

Advertiser Role
===============

.. autoclass:: bleson.core.roles.Advertiser
   :members:


.. note:: macOS implementation note

   You can only set the name and the services UUID's, and visbility of your advertiser depends on your app being a foreground process.

   See the CoreBluetooth_ documentation.

Observer Role
=============

.. autoclass:: bleson.core.roles.Observer
   :members:


.. _CoreBluetooth: https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/CoreBluetooth_concepts/BestPracticesForSettingUpYourIOSDeviceAsAPeripheral/BestPracticesForSettingUpYourIOSDeviceAsAPeripheral.html
