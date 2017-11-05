import abc


class Provider(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_adapter(cls, adapter_id=None):
        """Return an Adapter instance, default to first one available"""
        raise NotImplementedError
