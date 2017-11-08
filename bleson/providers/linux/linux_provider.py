from bleson.interfaces.provider import Provider
from .linux_adapter import BluetoothHCIAdapter
from bleson.logger import log


class LinuxProvider(Provider):

    def get_adapter(self, adapter_id=0):
        adapter = BluetoothHCIAdapter(adapter_id)
        adapter.open()
        adapter.off()
        adapter.on()
        return adapter

    # TODO: have a 'get_converter(for_type)' and registry of ValueObject to provider data converters (Linux uses core HCI)
