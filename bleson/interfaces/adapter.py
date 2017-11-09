import abc

class Adapter(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def open(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on(self):
        raise NotImplementedError

    @abc.abstractmethod
    def off(self):
        raise NotImplementedError

    @abc.abstractmethod
    def start_scanning(self):
        raise NotImplementedError

    @abc.abstractmethod
    def stop_scanning(self):
        raise NotImplementedError

    @abc.abstractmethod
    def start_advertising(self, advertisement, scan_response=None):
        raise NotImplementedError

    @abc.abstractmethod
    def stop_advertising(self):
        raise NotImplementedError
