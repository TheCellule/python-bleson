#!/usr/bin/env python3

# Experiment with calling XPC using the built-in Python 'ctypes' module.
# e.g. an attempt at a pure python port of https://github.com/matthewelse/pyxpcconnection


import ctypes
from time import sleep

#############################################################################
# libDispatch Wrapper


# Opaque structure use to pass areound 'dispatch_queue_t' C type
# see: https://stackoverflow.com/questions/5030730/is-it-acceptable-to-subclass-c-void-p-in-ctypes
class dispatch_queue_t(ctypes.Structure):
    pass

# Load the dispatch library
_lib = ctypes.cdll.LoadLibrary("/usr/lib/system/libdispatch.dylib")

_dispatch_queue_create = _lib.dispatch_queue_create
_dispatch_queue_create.argtypes = [ctypes.c_char_p, ctypes.c_int32]  # 2nd param is stuct, but we don't use it.
_dispatch_queue_create.restype = ctypes.POINTER(dispatch_queue_t)

def dispatch_queue_create(name):
    b_name = name.encode('utf-8')
    c_name = ctypes.c_char_p(b_name)
    return _dispatch_queue_create(c_name, ctypes.c_int32(0))




#############################################################################
# XPC Wrapper

# Opaque type
class xpc_connection(ctypes.Structure):
    pass

# Constants from header file /usr/include/xpc/connection.h
XPC_CONNECTION_MACH_SERVICE_PRIVILEGED = 1 << 1


xpc = ctypes.cdll.LoadLibrary("/usr/lib/system/libxpc.dylib")

_xpc_connection_create_mach_service = xpc.xpc_connection_create_mach_service
_xpc_connection_create_mach_service.argtypes = [ctypes.c_char_p, ctypes.POINTER(dispatch_queue_t), ctypes.c_int32]
_xpc_connection_create_mach_service.restype = ctypes.POINTER(xpc_connection)

def xpc_connection_create_mach_service(name, queue, flags):
    b_name = name.encode('utf-8')
    c_name = ctypes.c_char_p(b_name)
    return _xpc_connection_create_mach_service(c_name, queue, flags)





# see: https://developer.apple.com/documentation/xpc/1448781-xpc_connection_resume
_xpc_connection_resume = xpc.xpc_connection_resume
_xpc_connection_resume.argtypes = [ctypes.POINTER(xpc_connection)]
#_xpc_connection_resume.restype = None

def xpc_connection_resume(connection):
    _xpc_connection_resume(connection)



# Opaque type
class xpc_object_t(ctypes.Structure):
    pass


xpc_handler_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(xpc_object_t)) # 1st parameter is funtion return type


# see: https://developer.apple.com/documentation/xpc/1448805-xpc_connection_set_event_handler

_xpc_connection_set_event_handler = xpc.xpc_connection_set_event_handler
_xpc_connection_set_event_handler.argtypes = [ctypes.POINTER(xpc_connection), ctypes.POINTER(xpc_handler_t)]
#_xpc_connection_set_event_handler.argtypes = [ctypes.POINTER(xpc_connection), xpc_handler_t]

def xpc_connection_set_event_handler(connection, handler):
    _xpc_connection_set_event_handler(connection, xpc_handler_t(handler))

#############################################################################

queue = dispatch_queue_create('myqueue')
print(queue)


def handler(object):
    print('XPC handler')
    pass

xpc_connection = xpc_connection_create_mach_service('myxpc', queue, XPC_CONNECTION_MACH_SERVICE_PRIVILEGED)

xpc_connection_set_event_handler(xpc_connection, handler)


xpc_connection_resume(xpc_connection)


sleep(10)

