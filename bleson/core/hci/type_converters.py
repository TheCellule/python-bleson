import struct

from bleson.core.hci.constants import *
from bleson.core.hci.types import HCIPacket, HCIPayload
from bleson.core.types import Advertisement, BDAddress, UUID16, UUID128
from bleson.logger import log


def hex_string(data):
    return "".join("{:02x} ".format(x) for x in data)


def bytearray_to_hexstring(ba):
    return hex_string(ba)


def hexstring_to_bytearray(hexstr):
    """"
        hexstr:     e.g. "de ad be ef 00"
    """
    return bytearray.fromhex(hexstr)


def event_to_string(event_code):
    return HCI_EVENTS[event_code]


def parse_hci_event_packet(data):
    evtcode, length = struct.unpack("<BB", data[:2])
    if evtcode != EVT_LE_META_EVENT:
        return HCIPacket(event_to_string(evtcode), evtcode, None, data[3:], length - 1)
    else:
        subevtcode = struct.unpack("<B", data[2:3])[0]
        return HCIPacket(
            event_to_string(evtcode), evtcode, subevtcode, data[3:], length - 1
        )


def rssi_from_byte(rssi_unsigned):
    rssi = rssi_unsigned - 256 if rssi_unsigned > 127 else rssi_unsigned
    if rssi == 127:
        rssi = None  # RSSI Not available
    elif rssi >= 20:
        rssi = None  # Reserved range 20-126

    return rssi


class AdvertisingDataConverters(object):
    @classmethod
    def from_advertisement(cls, advertisement):
        if advertisement.raw_data:
            return advertisement.raw_data

        hci_payload = HCIPayload()

        # TODO: Advertisement should support __iter__

        # WARN: Although the order isn't important, the Python tests are (currently) order sensitive.

        if advertisement.flags:
            hci_payload.add_item(GAP_FLAGS, [advertisement.flags])

        if advertisement.uuid16s:
            hci_payload.add_item(GAP_UUID_16BIT_COMPLETE, advertisement.uuid16s)
            # TODO: incompleteuuid16s

        if advertisement.uuid128s:
            hci_payload.add_item(GAP_UUID_128BIT_COMPLETE, advertisement.uuid128s)
            # TODO: incompleteuuid128s

        if advertisement.tx_pwr_lvl:
            hci_payload.add_item(GAP_TX_POWER, advertisement.tx_pwr_lvl)

        if advertisement.name:
            # TODO: 'incomplete' name
            hci_payload.add_item(
                GAP_NAME_COMPLETE, advertisement.name.encode("ascii")
            )  # TODO: check encoding is ok

        # TODO: more!!

        return hci_payload.data

    @classmethod
    def from_hcipacket(cls, hci_packet: HCIPacket):
        """
            uint8_t		evt_type;
            uint8_t		bdaddr_type;
            bdaddr_t	bdaddr;
            uint8_t		length;
            uint8_t		data[0];
        """

        if (
            hci_packet.event_code != HCI_LE_META_EVENT
            and hci_packet.subevent_code != EVT_LE_ADVERTISING_REPORT
        ):
            raise ValueError("Invalid HCI Advertising Packet {}".format(hci_packet))

        return cls.from_hcipayload(hci_packet.data)

    @classmethod
    def from_extended_hcipacket(cls, hci_packet: HCIPacket):
        """
            uint16_t	evt_type;
            uint8_t		bdaddr_type;
            bdaddr_t	bdaddr;
            uint8_t		primary_phy;
            uint8_t		secondary_phy;
            uint8_t		advertising_sid;
            int8_t		tx_power;
            int8_t		rssi;
            uint16_t	periodic_advertising_interval;
            uint8_t		direct_address_type;
            bdaddr_t	direct_address;
            uint8_t		length;
            uint8_t		data[0];
        """

        if (
            hci_packet.event_code != HCI_LE_META_EVENT
            and hci_packet.subevent_code != EVT_LE_EXTENDED_ADVERTISING_REPORT
        ):
            raise ValueError("Invalid HCI Extended Advertising Packet {}".format(hci_packet))

        return cls.from_extended_hcipayload(hci_packet.data)

    @classmethod
    def from_hcipayload(cls, data):
        data_info = "Data: {}".format(hex_string(data))
        pos_info = "POS : {}".format(
            "".join("{:02} ".format(x) for x in range(0, len(data)))
        )
        log.debug(data_info)
        log.debug(pos_info)

        num_reports = data[0]
        log.debug("Num Reports {}".format(num_reports))

        if num_reports != 1:
            log.error(
                "TODO: Only 1 Advertising report is supported, creating empty Advertisement"
            )
            # don't make it fatal
            return Advertisement()

        # TODO: move these 2 LUTs to a better place
        gap_adv_type = [
            "ADV_IND",
            "ADV_DIRECT_IND",
            "ADV_SCAN_IND",
            "ADV_NONCONN_IND",
            "SCAN_RSP",
        ][data[1]]
        gap_addr_type = ["PUBLIC", "RANDOM", "PUBLIC_IDENTITY", "RANDOM_STATIC"][
            data[2]
        ]
        gap_addr = data[3:9]
        rssi = rssi_from_byte(data[-1])

        advertisement = Advertisement(address=BDAddress(gap_addr), rssi=rssi, raw_data=data)
        advertisement.type = gap_adv_type
        advertisement.address_type = gap_addr_type

        return AdvertisingDataConverters.parse_advertisement_data(
                advertisement, 10, len(data)-11)

    @classmethod
    def from_extended_hcipayload(cls, data):
        data_info = "Data: {}".format(hex_string(data))
        pos_info = "POS : {}".format(
            "".join("{:02} ".format(x) for x in range(0, len(data)))
        )
        log.debug(data_info)
        log.debug(pos_info)

        num_reports = data[0]
        log.debug("Num Reports {}".format(num_reports))

        if num_reports != 1:
            log.error(
                "TODO: Only 1 Advertising report is supported, creating empty Advertisement"
            )
            # don't make it fatal
            return Advertisement()

        if data[1] & 1 << 4:
            gap_adv_type = {
                    0x13: "ADV_IND",
                    0x15: "ADV_DIRECT_IND",
                    0x12: "ADV_SCAN_IND",
                    0x10: "ADV_NONCONN_IND",
                    0x1a: "SCAN_RSP_TO_ADV",
                    0x1b: "SCAN_RSP",
                    }[data[1]]
        else:
            gap_adv_type = []
            if data[1] & 1 << 0:
                gap_adv_type.append("Connectable")
            if data[1] & 1 << 1:
                gap_adv_type.append("Scannable")
            if data[1] & 1 << 2:
                gap_adv_type.append("Directed")
            if data[1] & 1 << 3:
                gap_adv_type.append("Scan Response")
            if data[1] & 1 << 5:
                gap_adv_type.append("Incomplete, more data to come")
            elif data[1] & 1 << 6:
                gap_adv_type.append("Incomplete, truncated")
            gap_adv_type = ','.join(gap_adv_type)
        # ignore data[2] - reserved for future use
        gap_addr_type = {
                0x00: "PUBLIC",
                0x01: "RANDOM",
                0x02: "PUBLIC_IDENTITY",
                0x03: "RANDOM_STATIC",
                0xff: "ANONYMOUS"}[
            data[3]
        ]
        gap_addr = data[4:10]
        primary_phy = {0x01: "LE 1M",
                       0x03: "LE Coded"
                      }[data[10]]
        secondary_phy = {0x00: "No",
                         0x01: "LE 1M",
                         0x02: "LE 2M",
                         0x03: "LE Coded"
                        }[data[11]]
        if data[12] == 0xff:
            advertising_sid = "no ADI field"
        else:
            advertising_sid = "NYI"
        if data[13] == 0x7f:
            tx_power = None
        else:
            tx_power = -127 + data[13] ## dBm
        rssi = rssi_from_byte(data[14])
        periodic_advertising_interval = ((data[16] << 16) + data[15]) * 1.25 ## ms
        direct_addr_type = {
                0x00: "PUBLIC",
                0x01: "STATIC",
                0x02: "RESOLVABLE_PRIVATE1",
                0x03: "RESOLVABLE_PRIVATE2",
                0xfe: "RESOLVABLE_PRIVATE_UNABLE_TO_RESOLVE"
                }[data[17]]
        direct_addr = data[18:24]

        advertisement = Advertisement(address=BDAddress(gap_addr), tx_power=tx_power, rssi=rssi, data_format="extended", raw_data=data)
        advertisement.type = gap_adv_type
        advertisement.address_type = gap_addr_type
        advertisement.primary_phy = primary_phy
        advertisement.secondary_phy = secondary_phy
        advertisement.periodic_advertising_interval = periodic_advertising_interval
        advertisement.direct_addr_type = direct_addr_type
        advertisement.direct_addr = direct_addr

        return AdvertisingDataConverters.parse_advertisement_data(
                advertisement, 25, data[24])

    @classmethod
    def parse_advertisement_data(cls, advertisement, init_pos, datalen):
        data = advertisement.raw_data
        data_info = "Data: {}".format(hex_string(data))
        pos_info = "POS : {}".format(
            "".join("{:02} ".format(x) for x in range(0, len(data)))
        )
        log.debug(data_info)
        log.debug(pos_info)
        pos = init_pos
        while pos < init_pos + datalen:
            log.debug("POS={}".format(pos))
            length = data[pos]
            gap_type = data[pos + 1]
            payload = data[pos + 2 : pos + 2 + length - 1]
            log.debug(
                "Pos={} Type=0x{:02x} Len={} Payload={}".format(
                    pos, gap_type, length, hex_string(payload)
                )
            )

            if GAP_FLAGS == gap_type:
                advertisement.flags = payload[0]
                log.debug("Flags={:02x}".format(advertisement.flags))

            elif GAP_UUID_16BIT_COMPLETE == gap_type:
                uuids = []
                byte_pos = 0
                if len(payload) % 2 != 0:
                    raise ValueError("PAyload is not divisible by 2 for UUID16")

                while byte_pos < len(payload):
                    log.debug("byte_pos={}".format(byte_pos))
                    byte_pair = payload[byte_pos : byte_pos + 2]
                    log.debug("byte pair = {}".format(byte_pair))
                    uuid = UUID16(byte_pair)
                    uuids.append(uuid)
                    byte_pos += 2

                advertisement.uuid16s = uuids

            elif GAP_UUID_128BIT_INCOMPLETE == gap_type:
                # if length-1 > 16:
                #     log.warning("TODO: >1 UUID128's found, not yet split into individual elements")
                # advertisement.uuid128s=[UUID128(payload)]
                uuids = []
                byte_pos = 0
                if len(payload) % 16 != 0:
                    raise ValueError("Payload is not divisible by 16 for UUID128")

                while byte_pos < len(payload):
                    log.debug("byte_pos={}".format(byte_pos))
                    byte_list = payload[byte_pos : byte_pos + 16]
                    log.debug("byte_list = {}".format(byte_list))
                    uuid = UUID128(byte_list)
                    uuids.append(uuid)
                    byte_pos += 16

                advertisement.uuid128s_incomplete = uuids

                log.debug(advertisement.uuid128s_incomplete)

            elif GAP_UUID_128BIT_COMPLETE == gap_type:

                # if length-1 > 16:
                #     log.warning("TODO: >1 UUID128's found, not yet split into individual elements")
                # advertisement.uuid128s=[UUID128(payload)]
                uuids = []
                byte_pos = 0
                if len(payload) % 16 != 0:
                    raise ValueError("Payload is not divisible by 16 for UUID128")

                while byte_pos < len(payload):
                    log.debug("byte_pos={}".format(byte_pos))
                    byte_list = payload[byte_pos : byte_pos + 16]
                    log.debug("byte_list = {}".format(byte_list))
                    uuid = UUID128(byte_list)
                    uuids.append(uuid)
                    byte_pos += 16

                advertisement.uuid128s = uuids

                log.debug(advertisement.uuid128s)

            elif GAP_NAME_INCOMPLETE == gap_type:
                advertisement.name = payload
                advertisement.name_is_complete = False
                log.debug("Incomplete Name={}".format(advertisement.name))

            elif GAP_NAME_COMPLETE == gap_type:
                advertisement.name = payload
                advertisement.name_is_complete = True
                log.debug("Complete Name={}".format(advertisement.name))

            elif GAP_SERVICE_DATA == gap_type:
                advertisement.service_data = payload
                log.debug("Service Data={}".format(advertisement.service_data))

            elif GAP_MFG_DATA == gap_type:
                advertisement.mfg_data = payload
                log.debug("Manufacturer Data={}".format(advertisement.mfg_data))

            elif GAP_TX_POWER == gap_type:
                if payload == None:
                    advertisement.tx_pwr_lvl = payload
                else:
                    advertisement.tx_pwr_lvl = int.from_bytes(
                        payload, byteorder="little"
                    )
                log.debug("TX Power={}".format(advertisement.tx_pwr_lvl))

            elif GAP_APPEARANCE == gap_type:
                # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.gap.appearance.xml
                # "The external appearance of this device. The values are composed of a category (10-bits) and sub-categories (6-bits)."
                # TODO: Add Appearance Names as well as IDs likey as "appearance: {id: , description:}"
                advertisement.appearance = int.from_bytes(payload, byteorder="little")
                log.debug("GAP Appearance={}".format(advertisement.appearance))

            else:
                log.warning(
                    "TODO: Unhandled GAP type, pos={} type=0x{:02x} len={}".format(
                        pos, gap_type, length
                    )
                )
                log.warning(data_info)
                log.warning(pos_info)

            pos += length + 1

        log.debug(advertisement)
        return advertisement
