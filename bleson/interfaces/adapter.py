import abc

class Adapter(object):
    """ Adapter interface
    """
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def open(self):
        """Initialise the adapter."""

        raise NotImplementedError

    @abc.abstractmethod
    def on(self):
        """Power on the adapter hardware."""

        raise NotImplementedError

    @abc.abstractmethod
    def off(self):
        """Power off the adapter hardware."""
        raise NotImplementedError

    @abc.abstractmethod
    def start_scanning(self):
        """Start BLE scanning."""

        raise NotImplementedError

    @abc.abstractmethod
    def stop_scanning(self):
        """Stop BLE scanning."""
        raise NotImplementedError

    @abc.abstractmethod
    def start_advertising(self, advertisement, scan_response=None):
        """Start BLE advertising."""

        raise NotImplementedError

    @abc.abstractmethod
    def stop_advertising(self):
        """Stop BLE advertising."""

        raise NotImplementedError
