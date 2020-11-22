from bleson.logger import log
from uuid import UUID

# Collection of value objects.

# They represent data types in the bluetooth spec.

# Object equlity is not based on the objects address, but instead for example, may be based on a MAC (BDAddress)

class ValueObject(object):

    def __bytes__(self):
        """Return bytes in little endian byte order."""

        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    # TODO: create from bytes, __init__


class UUID16(ValueObject):
    """ 16Bit UUID Type

        :param uuid: The 16bit uuid source value
        :param little_endian: Byte order, default True
        :type uuid: string, list, tuple, bytes or bytearray
        :type little_endian: bool

        .. testsetup:: *

           from bleson.core.types import UUID16

        Example of initialisation with a 16bit integer:

        .. testcode:: UUID16_INT

           print(UUID16(0xFFFF))

        Output:

        .. testoutput:: UUID16_INT

           UUID16(0xffff)


        Example of initialisation with a list:

        .. testcode:: UUID16_LIST

           print(UUID16([0x34, 0x12]))

        Output:

        .. testoutput:: UUID16_LIST

           UUID16(0x1234)
        """

    # Doctest example:
    # .. doctest:: UUID16
    #     >>> from bleson.core.types import UUID16
    #     >>> uuid=UUID16(0xffff)
    #     UUID16(0xfff0)

    def __init__(self, uuid, little_endian=True):

        log.debug(("UUID16 type: {} value={}".format(type(uuid), uuid)))
        if isinstance(uuid, memoryview):
            uuid = uuid.tolist()

        if isinstance(uuid, int):
            if not 0 <= uuid <= 0xffff:
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
    """ 128 Bit Type.

        :param uuid: The 16bit uuid source value
        :param little_endian: Byte order, default True
        :type uuid: string, list, tuple, bytes or bytearray
        :type little_endian: bool

        .. testsetup:: *

           from bleson.core.types import UUID128

        Example of initialisation with a list:

        .. testcode:: UUID128

           print(UUID128([0x23, 0xD1, 0xBC, 0xEA, 0x5F, 0x78, 0x23, 0x15, 0xDE, 0xEF, 0x12, 0x12, 0x30, 0x15, 0x00, 0x00]))

        Output:

        .. testoutput:: UUID128

           UUID128('00001530-1212-efde-1523-785feabcd123')


        Example of initialisation with a 16bit integer:

        .. testcode:: UUID128_INT

           print(UUID128(0x1234))

        Output:

        .. testoutput:: UUID128_INT

           UUID128('00001234-0000-1000-8000-00805f9b34fb')
    """
    def __init__(self, uuid, little_endian=True):
        """ Create UUID128, non-int types must be little endian (e.g. 'reversed' order w.r.t. displayed UUID)"""

        # TODO: accept 32bit and convert,  xxxxxxxx-0000-1000-8000-00805F9B34FB
        log.debug(("UUID128 type: {} value={}".format(type(uuid), uuid)))

        if isinstance(uuid, memoryview):
            uuid = uuid.tobytes()

        # Massage 'uuid' into a string that the built-in UUID() contructor accepts
        if isinstance(uuid, int):
            if not 0 <= uuid <= 0xffff:
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
    """ Bluetooth Device Address.

        :param address: The device bluetooth address
        :type uuid: string, list, tuple, bytes or bytearray
        :type little_endian: bool

        .. testsetup:: *

           from bleson.core.types import BDAddress

        Example of initialisation with a list:

        .. testcode:: BDADDRESS_LIST

           print(BDAddress([0xab, 0x90, 0x78, 0x56, 0x34, 0x12]))

        Output:

        .. testoutput:: BDADDRESS_LIST

           BDAddress('12:34:56:78:90:AB')


        Example of initialisation with a bytearray:

        .. testcode:: BDADDRESS_BYTEARRAY

           print(BDAddress(bytearray([0xab, 0x90, 0x78, 0x56, 0x34, 0x12])))

        Output:

        .. testoutput:: BDADDRESS_BYTEARRAY

           BDAddress('12:34:56:78:90:AB')


    """
    # TODO:  add an overide for little_endian=True\False flag, default True, for list-like types
    def __init__(self, address=None):
        if not address:
            address="00:00:00:00:00:00"             # TODO: is defaulting this a good idea?
        # expect a string of the format "xx:xx:xx:xx:xx:xx"
        # or a 6 element; tuple, list, bytes or bytearray
        if isinstance(address, str):
            # TODO: regex based check
            if len(address) != 6*2+5:
                raise ValueError('Unexpected address length of {} for {}'.format(len(address), address))
            address = address
        elif isinstance(address, list) \
                or isinstance(address, tuple) \
                or isinstance(address, bytes) \
                or isinstance(address, bytearray):
            if len(address) != 6:
                raise ValueError('Unexpected address length of {} for {}'.format(len(address), address))
            address =':'.join([format(c, '02x') for c in list(reversed(address))])
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
    """ Bluetooth LE Device Info.

       :param address: Bluetooth Device Address
       :param name: device name
       :param rssi: device RSSI
       :type address: BDAddress
       :type name: str
       :type rssi: integer

       .. testsetup:: *

          from bleson.core.types import Device, BDAddress

       Example of initialisation with list:

       .. testcode:: DEVICE

          print(Device(address=BDAddress('12:34:56:78:90:AB'), name='bleson', rssi=-99))

       Output:

       .. testoutput:: DEVICE

          Device(address=BDAddress('12:34:56:78:90:AB'), name='bleson', rssi=-99)

       """
    def __init__(self, address:BDAddress=None, name=None, rssi=None):
        self.address = address
        self.name = name
        self.rssi = rssi
        log.debug(self)

    def __repr__(self):
        return "Device(address={}, name='{}', rssi={})".format(self.address, self.name, self.rssi)

    def __eq__(self, other):
        return isinstance(other, Device) and self.address == other.address

    def __hash__(self):
        return hash(self.address)


class Advertisement(ValueObject):
    """ Bluetooth LE AdvertisementReport

       :param address: Bluetooth Device Adress
       :param name: device name
       :param rssi: device RSSI
       :param tx_power: device transmit power
       :param raw_data: pre-rolled advertisement payload
       :type address: BDAddress
       :type name: str
       :type rssi: integer
       :type tx_power: integer
       :type raw_data: bytearray on Linux (HCI data) or a dictionary on macOS/Win

       .. testsetup:: *

          from bleson.core.types import Advertisement, BDAddress

       Example of initialisation with list:

       .. testcode:: ADV_REPORT_1

          print(Advertisement(address=BDAddress('12:34:56:78:90:AB'), name='bleson', rssi=-99, tx_power=0))

       Output:

       .. testoutput:: ADV_REPORT_1

          Advertisement(flags=0x06, name='bleson', txpower=0, uuid16s=[], uuid128s=[], rssi=-99, mfg_data=None)

       """
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
        return "Advertisement(flags=0x{:02x}, name='{}', txpower={}, uuid16s={}, uuid128s={}, rssi={}, mfg_data={})".format(
            self.flags, self.name, self.tx_pwr_lvl, self.uuid16s, self.uuid128s, self.rssi, self.mfg_data)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, bytearray) or isinstance(name, bytes):
            try:
                self._name = str(name, encoding='utf-8')  # UTF-8 (BLE core spec)
            except UnicodeDecodeError as e:
                log.warning("Name is not a valid UTF-8 string")
                self._name = name   # make the invalid name available still
        else:
            self._name = str(name)  # unit8


class ScanResponse(Advertisement):
    pass


