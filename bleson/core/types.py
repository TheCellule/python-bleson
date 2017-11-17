from bleson.logger import log
from uuid import UUID

# Collection of value objects.

# They represent data types in the bluetooth spec.

# Object equlity is not based on the objects address, but instead for example, may be based on a MAC (BDAddress)

class ValueObject(object):

    def __bytes__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    # TODO: create from bytes, __init__


class UUID16(ValueObject):

    def __init__(self, uuid, little_endian=True):
        """ Create UUID16, non-int types are assumed to be little endian (reverse order)"""

        log.debug(("UUID16 type: {} value={}".format(type(uuid), uuid)))
        if isinstance(uuid, memoryview):
            uuid = uuid.tolist()

        if isinstance(uuid, int):
            if not 0 < uuid < 0xffff:
                raise ValueError('Invalid UUID16 value {}'.format(uuid))

        elif isinstance(uuid, list) or isinstance(uuid, tuple):
            if len(uuid) != 2:
                raise ValueError('Unexpected address length of {} for {}'.format(len(uuid), uuid))
            uuid = (uuid[1] << 8) + (uuid[0] & 0xff)
        elif isinstance(uuid, bytes) or isinstance(uuid, bytearray):
            if len(uuid) != 2:
                raise ValueError('Unexpected address length of {} for {}'.format(len(uuid), uuid))
            uuid = (uuid[1] << 8) + (uuid[0] & 0xff)
        else:
            raise TypeError('Unsupported UUID16 initialiser type: {}'.format(type(uuid)))

        if not little_endian: # swap
            uuid = ( (uuid & 0xff) << 8 )  |  ( (uuid & 0xff00) >>8)
        self._uuid=uuid
        log.debug(self)

    def __hash__(self):
        return self._uuid

    def __eq__(self, other):
        return isinstance(other, UUID16) and self._uuid == other._uuid

    def __repr__(self):
        return "UUID16(0x{:02x})".format(self._uuid)

    def __bytes__(self):
        return bytes([self._uuid & 0xff, (self._uuid >>8) & 0xff])

    def __len__(self):
        return 2

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        raise NotImplemented


class UUID128(ValueObject):

    def __init__(self, uuid, little_endian=True):
        """ Create UUID128, non-int types must be little endian (e.g. 'reversed' order w.r.t. displayed UUID)"""

        # TODO: accept 32bit and convert,  xxxxxxxx-0000-1000-8000-00805F9B34FB
        log.debug(("UUID128 type: {} value={}".format(type(uuid), uuid)))

        if isinstance(uuid, memoryview):
            uuid = uuid.tobytes()

        # Massage 'uuid' into a string that the built-in UUID() contructor accepts
        if isinstance(uuid, int):
            if not 0 < uuid < 0xffff:
                raise ValueError('Invalid UUID16 value {} fro UUID128 promotion'.format(uuid))
            uuid = UUID("0000{:04x}-0000-1000-8000-00805F9B34FB".format(uuid)).hex

        elif isinstance(uuid, str):
            if not len(uuid) == 36:
                raise ValueError('Invalid UUID128 value {}'.format(uuid))

        elif isinstance(uuid, list) or isinstance(uuid, tuple) or isinstance(uuid, bytes) or isinstance(uuid, bytearray):
            if len(uuid) != 16:
                raise ValueError('Unexpected address length of {} for {}'.format(len(uuid), uuid))
            uuid = ''.join([format(c, '02x') for c in reversed(uuid)] )
        else:
            raise TypeError('Unsupported UUID128 initialiser type: {}'.format(type(uuid)))


        self._uuid_obj = UUID(uuid)

        if not little_endian:
            self._uuid_obj = UUID(bytes=bytes(reversed(self._uuid_obj.bytes)))


        self._uuid=self._uuid_obj.urn.replace('urn:uuid:', '')
        log.debug(self)

    def __hash__(self):
        return self._uuid

    def __eq__(self, other):
        return isinstance(other, UUID128) and self._uuid == other._uuid

    def __repr__(self):
        return "UUID128('{}')".format(self._uuid)


    def __bytes__(self):
        return bytes(reversed(self._uuid_obj.bytes))

    def __len__(self):
        return len(self._uuid_obj.bytes)

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        raise NotImplemented


class BDAddress(ValueObject):

    # TODO:  add an overide for little_endian=True\False flag, default True, for list-like types
    def __init__(self, address:str=None):
        # expect a string of the format "xx:xx:xx:xx:xx:xx"
        # or a 6 element; tuple, list, bytes or bytearray
        if isinstance(address, str):
            # TODO: regex based check
            if len(address) != 6*2+5:
                raise ValueError('Unexpected address length of {} for {}'.format(len(address, address)))
            address = address
        elif isinstance(address, list) or isinstance(address, tuple):
            if len(address) != 6:
                raise ValueError('Unexpected address length of {} for {}'.format(len(address, address)))
            address = "%02x:%02x:%02x:%02x:%02x:%02x" % address
        elif isinstance(address, bytes) or isinstance(address, bytearray):
            if len(address) != 6:
                raise ValueError('Unexpected address length of {} for {}'.format(len(address, address)))
            address = ':'.join([format(c, '02x') for c in address])
        else:
            raise TypeError('Unsupported address type: {}'.format(type(address)))

        # TODO:  keep this for hashing but return bytearray for getter (defaulted to little endian)
        self.address=address.upper()
        log.debug(self)

    def __repr__(self):
        return "BDAddress('{}')".format(self.address)

    def __eq__(self, other):
        return isinstance(other, BDAddress) and self.address == other.address

    def __hash__(self):
        return hash(self.address)


class Device(ValueObject):

    def __init__(self, address:BDAddress=None, name=None, rssi=None):
        self.address = address
        self.name = name
        self.rssi = rssi
        log.debug(self)

    def __repr__(self):
        return "Device(address={}, name={}, rssi={})".format(self.address, self.name, self.rssi)

    def __eq__(self, other):
        return isinstance(other, Device) and self.address == other.address

    def __hash__(self):
        return hash(self.address)


class Advertisement(ValueObject):

    def __init__(self, name=None, address=None, rssi=None, tx_power=None, raw_data=None):
        #TODO: use kwargs
        self.flags      =   6   # uint8         # default to LE_GENERAL_DISCOVERABLE | BREDR_NOT_SUPPORTED
        self.type = None
        self.address_type = None
        self.address = address
        self._name = name
        self.name_is_complete   = False     # unsigned
        self.tx_pwr_lvl = tx_power  # unsigned
        self.appearance     = None      # unit16
        self.uuid16s    =   []  # uuid16[]
        self.uuid32s    =   []  # uuid32[]
        self.uuid128s   =   []  # uuid12[]
        self.service_data = None
        #slave_itvl_range
        self.svc_data_uuid16 = None       # uuid16[]
        self.public_tgt_addr = None       #  uint8[]
        self.adv_itvl = None        # uint16
        self.svc_data_uuid32 = None # uint8
        self.svc_data_uuid128 = None # uint8
        self.uri    =   None        # unit8
        self.mfg_data = None        # unit8
        self.rssi = rssi            # really only part of an Advertisement Report...

        self.raw_data = raw_data
        log.debug(self)


    def __repr__(self):
        # TODO: appearance etc...
        return "Advertisement(flags=0x{:02x}, name={}, txpower={} uuid16s={} uuid128s={} rssi={} mfg_data={})".format(
            self.flags, self.name, self.tx_pwr_lvl, self.uuid16s, self.uuid128s, self.rssi, self.mfg_data)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, bytearray):
            self._name = str(name,'ascii')  # TODO: is the name really UTF8 encoded according to the Core spec?
        else:
            self._name = str(name)  # unit8


class ScanResponse(Advertisement):
    pass


