from bleson.core.hci import rssi_from_byte
from bleson.core.hci.constants import *
from bleson.core.hci.types import HCIPacket, HCIPayload
from bleson.core.types import Advertisement, BDAddress
from bleson.logger import log
from bleson.utils import hex_string, bytearray_to_hexstring

# meh...

class AdvertisingDataConverters(object):

    @classmethod
    def from_advertisement(cls, advertisement):
        if advertisement.raw_data:
            return advertisement.raw_data

        hci_payload = HCIPayload()

        #TODO: Advertisement should support __iter__

        if advertisement.flags:
            hci_payload.add_item(GAP_FLAGS, [advertisement.flags])
        if advertisement.name:
            hci_payload.add_item(GAP_NAME_COMPLETE, advertisement.name.encode('ascii'))

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

        if hci_packet.event_code != HCI_LE_META_EVENT and hci_packet.subevent_code != EVT_LE_ADVERTISING_REPORT:
            raise ValueError("Invalid HCI Advertising Packet {}".format(hci_packet))

        return cls.from_hcipayload(hci_packet.data)

    @classmethod
    def from_hcipayload(cls, data):
        data_info = "Data: {}".format(hex_string(data))
        pos_info = "POS : {}".format(''.join('{:02} '.format(x) for x in range(0, len(data))))
        log.debug(data_info)
        log.debug(pos_info)

        num_reports = data[0]
        log.debug("Num Reports {}".format(num_reports))

        if num_reports !=1:
            log.error("TODO: Only 1 Advertising report is supported, creating emtpy Advertisement")
            # don't make it fatal
            return Advertisement()

        gap_adv_type = ['ADV_IND', 'ADV_DIRECT_IND', 'ADV_SCAN_IND', 'ADV_NONCONN_IND', 'SCAN_RSP'][data[1]]
        gap_addr_type = ['PUBLIC', 'RANDOM', 'PUBLIC_IDENTITY', 'RANDOM_STATIC'][data[2]]
        gap_addr = data[8:2:-1]
        rssi = rssi_from_byte(data[-1])


        advertisement = Advertisement(address=BDAddress(gap_addr), rssi=rssi)
        advertisement.type = gap_adv_type
        advertisement.address_type = gap_addr_type

        pos = 10
        while pos < len(data)-1:
            log.debug("POS={}".format(pos))
            length = data[pos]
            gap_type = data[pos+1]
            payload = data[pos+2:pos+2+length-1]
            log.debug("Pos={} Type=0x{:02x} Len={} Payload={}".format(pos, gap_type, length, hex_string(payload)))

            if GAP_FLAGS == gap_type:
                advertisement.flags = payload[0]
                log.debug("Flags={:02x}".format(advertisement.flags))

            elif GAP_UUID_16BIT_COMPLETE == gap_type:
                #
                if length-1 > 2:
                    log.warning("TODO: >1 UUID16's found, not yet split into individual elements")
                advertisement.uuid16s=[payload]

            elif GAP_UUID_128BIT_COMPLETE == gap_type:
                #
                #if length-1 > 2:
                #    log.warning("TODO: >1 UUID128's found, not yet split into individual elements")
                advertisement.uuid128s=[payload]
                log.debug(bytearray_to_hexstring(advertisement.uuid128s[0]))

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

            else:
                log.warning("TODO: Unhandled GAP type, pos={} type=0x{:02x} len={}".format(pos, gap_type, length))
                log.warning(data_info)
                log.warning(pos_info)

            pos += length +1


        log.debug(advertisement)
        return advertisement
