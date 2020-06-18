from bleson.interfaces.provider import Provider
from .stub_adapter import BluetoothAdapter

class StubProvider(Provider):

    def get_adapter(self, adapter_id=0):
        adapter = BluetoothAdapter(adapter_id)
        return adapter
