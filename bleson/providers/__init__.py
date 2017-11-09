import sys

from bleson.logger import log

_provider = None


def get_provider():

    global _provider

    if _provider is None:
        if sys.platform.startswith('linux'):
            from bleson.providers.linux.linux_provider import LinuxProvider
            _provider = LinuxProvider()
        elif sys.platform.startswith('darwin'):
            from bleson.providers.macos.macos_provider import MacOSProvider
            _provider = MacOSProvider()

        elif sys.platform.startswith('win32'):
            raise NotImplementedError()
        else:
            raise RuntimeError('Platform {0} is not supported!'.format(sys.platform))

    log.info("Provider is {}".format(_provider))

    return _provider
