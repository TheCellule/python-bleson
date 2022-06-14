import array
import fcntl
import socket
import struct
import threading

from bleson.core.hci.constants import *
from bleson.core.hci.type_converters import AdvertisingDataConverters, parse_hci_event_packet, hex_string
from bleson.core.types import Device, BDAddress
from bleson.interfaces.adapter import Adapter
from bleson.logger import log
from .constants import *


class BluetoothHCIAdapter(Adapter):

    def __init__(self, device_id=0):
        self.device_id = device_id
        self._keep_running = True
        self._socket = None
        self._socket_poll_thread = None

        # User callbacks
        self.on_advertising_data = None

    def __del__(self):
        self._keep_running = False


    def open(self):
        self._socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
        self._socket.bind((self.device_id,))
        self._le_features = threading.Condition()
        self._socket_poll_thread = threading.Thread(target=self._socket_poller, name='HCISocketPoller')
        self._socket_poll_thread.setDaemon(True)
        self._socket_poll_thread.start()
        self.device = self.get_device_info()

    def close(self):
        self._socket.close()

    def send_cmd(self, cmd, data):
        arr = array.array('B', data)
        fcntl.ioctl(self._socket.fileno(), cmd, arr)
        return arr

    def send_cmd_value(self, cmd, value):
        fcntl.ioctl(self._socket.fileno(), cmd, value)

    def write_buffer(self, data):
        log.debug(data)
        self._socket.send(data)

    def _set_filter(self, data):
        self._socket.setsockopt(socket.SOL_HCI, socket.HCI_FILTER, data)

    def _reset_filter(self):
        self._set_filter(self._last_filter)

    def _socket_poller(self):
        while self._keep_running:
            data = self._socket.recv(1024)         # blocking
            try:
                self._on_data(data)
            except Exception:
                log.exception("Exception ignored in HCISocketPoller")

    # Adapter INfo

    def get_device_info(self):

        # C hci_dev_info struct defined at https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/lib/hci.h#n2382
        hci_dev_info_struct = struct.Struct('=H 8s 6B L B 8B 3L 4I 10L')

        request_dta = hci_dev_info_struct.pack(
            self.device_id,
            b'',
            0, 0, 0, 0, 0, 0,
            0,
            0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        response_data = self.send_cmd(HCIGETDEVINFO, request_dta)

        hci_dev_info = hci_dev_info_struct.unpack(response_data)

        # Just extract a few parts for now
        device_id = hci_dev_info[0]
        device_name = hci_dev_info[1].split(b'\0',1)[0]
        bd_address = hci_dev_info[2:8]
        return Device(address=BDAddress(bd_address), name=device_name)

    def has_extended_advertising(self):
        if hasattr(self, 'extended_advertising'):
            return self.extended_advertising
        else:
            self.sync_read_le_local_features()
            return self.extended_advertising

    def sync_read_le_local_features(self):
        self._le_features.acquire()
        self.set_features_filter()
        cmd = struct.pack("<BHB", HCI_COMMAND_PKT, LE_READ_LOCAL_SUPPORTED_FEATURES, 0)
        self.write_buffer(cmd)
        self._le_features.wait()

    def set_features_filter(self):
        typeMask   = 1 << HCI_EVENT_PKT
        eventMask1 = (1 << EVT_CMD_COMPLETE) | (1 << EVT_CMD_STATUS)
        eventMask2 = 0
        opcode     = 0

        self._last_filter = self._socket.getsockopt(socket.SOL_HCI, socket.HCI_FILTER)
        filter = struct.pack("<LLLH", typeMask, eventMask1, eventMask2, opcode)
        self._set_filter(filter)

    # -------------------------------------------------
    # Adapter power control

    def on(self):
        self.send_cmd_value(HCIDEVUP, self.device_id)

    def off(self):
        self.send_cmd_value(HCIDEVDOWN, self.device_id)

    # -------------------------------------------------
    # Scanning

    def set_scan_filter(self):
        typeMask   = 1 << HCI_EVENT_PKT
        eventMask1 = (1 << EVT_CMD_COMPLETE) | (1 << EVT_CMD_STATUS)
        eventMask2 = 1 << (EVT_LE_META_EVENT - 32)
        opcode     = 0

        filter = struct.pack("<LLLH", typeMask, eventMask1, eventMask2, opcode)
        self._set_filter(filter)

    def set_scan_parameters(self):
        if self.has_extended_advertising():
            self.set_extended_scan_parameters()
        else:
            self.set_simple_scan_parameters()

    def set_simple_scan_parameters(self):
        len = 7
        type = SCAN_TYPE_ACTIVE
        internal = 0x0010   #  ms * 1.6
        window = 0x0010     #  ms * 1.6
        own_addr  = LE_PUBLIC_ADDRESS
        filter = FILTER_POLICY_NO_WHITELIST
        cmd = struct.pack("<BHBBHHBB", HCI_COMMAND_PKT, LE_SET_SCAN_PARAMETERS_CMD, len,
                          type, internal, window, own_addr, filter )
        self.write_buffer(cmd)

    def set_extended_scan_parameters(self):
        len = 8
        own_addr = LE_PUBLIC_ADDRESS
        filter = FILTER_POLICY_NO_WHITELIST
        phys = 0x01
        type = SCAN_TYPE_ACTIVE
        interval = 0x0010   #  ms * 1.6
        window = 0x0010     #  ms * 1.6
        cmd = struct.pack("<BHBBBBBHH", HCI_COMMAND_PKT, LE_SET_EXTENDED_SCAN_PARAMETERS_CMD,
                          len, own_addr, filter, phys, type, interval, window)
        self.write_buffer(cmd)

    def set_scan_enable(self, enabled=False, filter_duplicates=False):
        if self.has_extended_advertising():
            self.set_extended_scan_enable(enabled, filter_duplicates)
        else:
            self.set_simple_scan_enable(enabled, filter_duplicates)

    def set_simple_scan_enable(self, enabled, filter_duplicates):
        len = 2
        enable = 0x01 if enabled else 0x00
        dups   = 0x01 if filter_duplicates else 0x00
        cmd = struct.pack("<BHBBB", HCI_COMMAND_PKT, LE_SET_SCAN_ENABLE_CMD, len, enable, dups)
        self.write_buffer(cmd)

    def set_extended_scan_enable(self, enabled, filter_duplicates):
        len = 6
        enable = 0x01 if enabled else 0x00
        dups   = 0x01 if filter_duplicates else 0x00
        duration = 0x0000
        period = 0x0000
        cmd = struct.pack("<BHBBBHH", HCI_COMMAND_PKT, LE_SET_EXTENDED_SCAN_ENABLE_CMD,
                          len, enable, dups, duration, period)
        self.write_buffer(cmd)

    # -------------------------------------------------
    # Advertising

    def set_advertising_filter(self):
        typeMask   = 1 << HCI_EVENT_PKT | (1 << HCI_ACLDATA_PKT)
        eventMask1 = 1 << EVT_DISCONN_COMPLETE | (1 << EVT_CMD_COMPLETE) | (1 << EVT_CMD_STATUS)
        eventMask2 = 1 << (EVT_LE_META_EVENT - 32)
        opcode     = 0

        filter = struct.pack("<LLLH", typeMask, eventMask1, eventMask2, opcode)
        self._set_filter(filter)

    def set_advertise_enable(self, enabled):
        cmd = struct.pack("<BHBB",
                          HCI_COMMAND_PKT,
                          LE_SET_ADVERTISE_ENABLE_CMD,
                          1,            # cmd parameters length
                          0x01 if enabled else 0x00
                          )
        self.write_buffer(cmd)


    def set_advertising_parameter(self):
        cmd = struct.pack("<BHB" + "H H 3B 6B B B",
                          HCI_COMMAND_PKT,
                          LE_SET_ADVERTISING_PARAMETERS_CMD,
                          15,           # cmd parameters length
                          0x00a0,       # min interval
                          0x00a0,       # max interval
                          0,            # adv type
                          0,            # direct addr type
                          0,            # direct addr type
                          0,0,0,0,0,0,  # direct addr
                          0x07,
                          0x00
                          )
        self.write_buffer(cmd)

    def set_scan_response_data(self, data):
        padded_data = memoryview(data).tolist()
        padded_data.extend([0] * (31 - len(padded_data)))

        cmd = struct.pack("<BHB" + "B31B",
                          HCI_COMMAND_PKT,
                          LE_SET_SCAN_RESPONSE_DATA_CMD,
                          32,           # cmd parameters length
                          len(data),
                          *padded_data
                          )
        self.write_buffer(cmd)

    def set_advertising_data(self, data):
        padded_data = memoryview(data).tolist()
        padded_data.extend([0] * (31 - len(padded_data)))

        cmd = struct.pack("<BHB" + "B31B",
                          HCI_COMMAND_PKT,
                          LE_SET_ADVERTISING_DATA_CMD,
                          32,           # cmd parameters length
                          len(data),
                          *padded_data
                          )
        self.write_buffer(cmd)




    # -------------------------------------------------
    # Inbound event handler for all messages

    def _handle_command_complete(self, data):
        log.debug("EVT_CMD_COMPLETE")
        # TODO: unpack based on: https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/lib/hci.h#n1853

        if (data[5] << 8) + data[4] == LE_SET_SCAN_PARAMETERS_CMD:
            if data[6] == HCI_SUCCESS:
                log.debug('LE Scan Parameters Set');
            else:
                log.debug('LE Set Scan Parameters Error: 0x%x' % (data[6]))
        elif (data[5] << 8) + data[4] == LE_SET_SCAN_ENABLE_CMD:
            if data[6] == HCI_SUCCESS:
                log.debug('LE Scan Enable Set')
            else:
                log.debug('LE Set Scan Enable Error: 0x%x' % (data[6]))
        elif (data[5] << 8) + data[4] == LE_SET_EXTENDED_SCAN_PARAMETERS_CMD:
            if data[6] == HCI_SUCCESS:
                log.debug('LE Extended Scan Parameters Set');
            else:
                log.debug('LE Set Extended Scan Parameters Error: 0x%x' % (data[6]))
        elif (data[5] << 8) + data[4] == LE_SET_EXTENDED_SCAN_ENABLE_CMD:
            if data[6] == HCI_SUCCESS:
                log.debug('LE Extended Scan Enable Set')
            else:
                log.debug('LE Set Extended Scan Enable Error: 0x%x' % (data[6]))
        elif (data[5] << 8) + data[4] == LE_SET_ADVERTISING_PARAMETERS_CMD:
            if data[6] == HCI_SUCCESS:
                log.debug('LE Advertising Parameters Set')
            else:
                log.debug('LE Set Advertising Parameters Error: 0x%x' % (data[6]))
        elif (data[5] << 8) + data[4] == LE_SET_ADVERTISING_DATA_CMD:
            if data[6] == HCI_SUCCESS:
                log.debug('LE Advertising Data Set')
            else:
                log.debug('LE Set Advertising Data Error: 0x%x' % (data[6]))
        elif (data[5] << 8) + data[4] == LE_SET_SCAN_RESPONSE_DATA_CMD:
            if data[6] == HCI_SUCCESS:
                log.debug('LE Scan Response Data Set')
            else:
                log.debug('LE Set Scan Response Data Error: 0x%x' % (data[6]))
        elif (data[5] << 8) + data[4] == LE_SET_ADVERTISE_ENABLE_CMD:
            if data[6] == HCI_SUCCESS:
                log.debug('LE Advertise Enable Set')
            else:
                log.debug('LE Set Advertise Enable Error: 0x%x' % (data[6]))
        elif (data[5] << 8) + data[4] == LE_READ_LOCAL_SUPPORTED_FEATURES:
            self._le_features.acquire()
            if data[6] == HCI_SUCCESS:
                features, = struct.unpack("<Q", data[7:15])
                self.extended_advertising = bool(features & 1 << 12)
                log.debug('LE Local Supported Features: 0x%x' % (features))
                log.debug('extended advertising: %s' % (str(self.extended_advertising)))
            else:
                log.debug('LE Read Local Supported Features Error: 0x%x' % (data[6]))
            self._reset_filter()
            self._le_features.notify()
            self._le_features.release()

    def _handle_disconnection_complete(self, data):
        log.debug("EVT_DISCONN_COMPLETE")
        disconn_info = dict(
            status=data[3],
            handle=(data[5] << 8) + data[4],
            reason=data[6]
        )
        log.debug(disconn_info)

    def _handle_meta_event(self, hci_packet):

        log.debug("EVT_LE_META_EVENT")

        if hci_packet.subevent_code == EVT_LE_ADVERTISING_REPORT:
            log.debug('LE Advertising Report')
            if self.on_advertising_data:
                advertisement = AdvertisingDataConverters.from_hcipacket(hci_packet)
                self.on_advertising_data(advertisement)
        elif hci_packet.subevent_code == EVT_LE_EXTENDED_ADVERTISING_REPORT:
            log.debug('LE Extended Adversiting Report')
            if self.on_advertising_data:
                advertisement = AdvertisingDataConverters.from_extended_hcipacket(hci_packet)
                self.on_advertising_data(advertisement)
        else:
            log.warning("TODO: unhandled HCI Meta Event packet, type={}".format(hci_packet))

    def _on_data(self, data):
        log.debug("----------------------------------------------------------------------")
        log.debug("Socket data: len={}, data={}".format(len(data), hex_string(data)))

        if data[0] == HCI_EVENT_PKT:
            hci_event_packet = parse_hci_event_packet(data[1:])
            log.debug(hci_event_packet)

            if data[1] == EVT_CMD_COMPLETE:
                self._handle_command_complete(data)

            elif data[1] == EVT_DISCONN_COMPLETE:
                self._handle_disconnection_complete(data)

            elif data[1] == EVT_LE_META_EVENT:
                self._handle_meta_event(hci_event_packet)

            else:
                log.warning("TODO: unhandled HCI Event packet, type={}".format(hci_event_packet))
        else:
            log.warning("TODO: Unhandled HCI packet, type={}".format(data[0]))

    def start_scanning(self):
        self.set_scan_enable(False)
        self.set_scan_filter()
        self.set_scan_parameters()
        self.set_scan_enable(True, False)

    def stop_scanning(self):
        self.set_scan_enable(False)

    def start_advertising(self, advertisement, scan_response=None):
        self.set_advertising_filter()
        self.set_advertise_enable(False)
        self.set_advertising_parameter()

        self.set_advertising_data(AdvertisingDataConverters.from_advertisement(advertisement))

        if scan_response:
            log.warning("TODO: support setting scan response")
        #    self.set_scan_response_data(scan_response_data.data)

        self.set_advertise_enable(True)

    def stop_advertising(self):
        self.set_advertise_enable(False)

