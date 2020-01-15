
from bleson.interfaces.adapter import Adapter
from bleson.interfaces.role import Role


class Observer(Role):
    """ Observer """

    def __init__(self, adapter : Adapter, on_advertising_data=None):
        self.adapter = adapter
        self.adapter.on_advertising_data = on_advertising_data

    def start(self):
        """ Start the observer """

        self.adapter.start_scanning()

    def stop(self):
        self.adapter.stop_scanning()

    @property
    def on_advertising_data(self):
        return self.adapter.on_advertising_data

    @on_advertising_data.setter
    def on_advertising_data(self, cb):
        self.adapter.on_advertising_data=cb

    # Potential candidate to be a generator, maybe even an asyncio coroutine-generator?
    # def discover_devices(self, timeout=None, filter=lambda advertisement: True):
    #     pass

class Advertiser(Role):

    def __init__(self, adapter : Adapter, advertisement=None, scan_response=None):
        self.adapter = adapter
        self.advertisement = advertisement
        self.scan_response = scan_response

    def start(self):
        self.adapter.start_advertising(self.advertisement, self.scan_response)

    def stop(self):
        self.adapter.stop_advertising()


