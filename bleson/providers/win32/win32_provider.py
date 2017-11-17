from bleson.interfaces.provider import Provider
from .win32_adapter import BluetoothAdapter
from bleson.logger import log

class Win32Provider(Provider):

    def get_adapter(self, adapter_id=0):
        adapter = BluetoothAdapter(adapter_id)
        adapter.open()
        adapter.off()
        adapter.on()
        return adapter

    # TODO: have a 'get_converter(for_type)' and registry of ValueObject to provider data converters (Linux uses core HCI)
