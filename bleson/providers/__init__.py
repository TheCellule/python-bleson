import logging
import sys

from bleson.logger import log

_provider = None

def get_provider():
    global _provider

    if _provider is None:
        if sys.platform.startswith('linux'):
            from bleson.providers.linux.linux_provider import LinuxProvider
            _provider = LinuxProvider()
        elif sys.startswith('darwin'):
            raise NotImplementedError()
        elif sys.startswith('win32'):
            raise NotImplementedError()
        else:
            raise RuntimeError('Platform {0} is not supported!'.format(sys.platform))

    return _provider
