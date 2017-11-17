from bleson.interfaces.provider import Provider
from .macos_adapter import CoreBluetoothAdapter
from bleson.logger import log


class MacOSProvider(Provider):

    def get_adapter(self, adapter_id=0):
        adapter = CoreBluetoothAdapter(adapter_id)
        adapter.open()
        adapter.off()
        adapter.on()
        return adapter

    # TODO: have a 'get_converter(for_type)' and registry of ValueObject to provider data converters (Linux uses core HCI)
