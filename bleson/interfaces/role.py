import abc

class Role(object):
    __metaclass__ = abc.ABCMeta

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    @abc.abstractmethod
    def start(self):
        """Start the role."""
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self):
        """Stop the role."""
        raise NotImplementedError
