from bleson.logger import log

# Collection of value objects.

# They represent data types in the bluetooth spec.

# Object equlity is not based on the objects address, but instead for example, may be based on a MAC (BDAddress)

class ValueObject(object):
    pass

    # speculative... better placed elsewhere...
    # def from_hci(self):
    #     pass
    #
    # def to_hci(self):
    #     pass


class BDAddress(ValueObject):

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
        self.uuid16s    =   None  # uuid16[]
        self.uuid32s    =   None  # uuid32[]
        self.uuid128s   =   None  # uuid12[]
        self.name = name
        self.name_is_complete   = False     # unsigned
        self.tx_pwr_lvl = tx_power  # unsigned
        #slave_itvl_range
        self.svc_data_uuid16 = None       # uuid16[]
        self.public_tgt_addr = None       #  uint8[]
        self.appearance     = None      # unit16
        self.adv_itvl = None        # uint16
        self.svc_data_uuid32 = None # uint8
        self.svc_data_uuid128 = None # uint8
        self.uri    =   None        # unit8
        self.mfg_data = None        # unit8
        self.service_data = None    # TODO: check this...
        self.type = None
        self.address_type = None
        self.address = address
        self.eir = None
        self.rssi = rssi

        self.raw_data = raw_data
        log.debug(self)


    def __repr__(self):
        # TODO: UUID's, appearance etc...
        return "Advertisement(flags=0x{:02x}, name={}, rssi={})".format(self.flags, self.name, self.rssi)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, bytearray):
            self._name = str(name,'ascii')  # TODO: is the name really UTF8 encoded according to the Core spec?
        else:
            self._name = str(name)  # unit8


class ScanResponse(ValueObject):
    pass


