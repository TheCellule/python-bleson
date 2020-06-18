
LE_PUBLIC_ADDRESS = 0x00
LE_RANDOM_ADDRESS = 0x01

# Types of bluetooth scan

SCAN_TYPE_PASSIVE = 0x00
SCAN_TYPE_ACTIVE  = 0x01
SCAN_FILTER_DUPLICATES = 0x01
SCAN_DISABLE = 0x00
SCAN_ENABLE = 0x01


# Advertisement event types
ADV_IND = 0x00
ADV_DIRECT_IND = 0x01
ADV_SCAN_IND = 0x02
ADV_NONCONN_IND = 0x03
ADV_SCAN_RSP = 0x04

FILTER_POLICY_NO_WHITELIST = 0x00  # Allow Scan Request from Any, Connect Request from Any
FILTER_POLICY_SCAN_WHITELIST = 0x01  # Allow Scan Request from White List Only, Connect Request from Any
FILTER_POLICY_CONN_WHITELIST = 0x02  # Allow Scan Request from Any, Connect Request from White List Only
FILTER_POLICY_SCAN_AND_CONN_WHITELIST = 0x03  # Allow Scan Request from White List Only, Connect Request from White List Only


EVT_CMD_COMPLETE = 0x0e
EVT_CMD_STATUS = 0x0f



# sub-events of LE_META_EVENT
EVT_LE_CONN_COMPLETE = 0x01

EVT_LE_ADVERTISING_REPORT = 0x02
EVT_LE_CONN_UPDATE_COMPLETE = 0x03
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE = 0x04
EVT_DISCONN_COMPLETE = 0x05
EVT_LE_META_EVENT = 0x3e            # Core_4.2.pdf section: 7.7.65 LE Meta Event


ATT_CID = 0x0004


ACL_START = 0x02


OGF_LE_CTL = 0x08
OGF_LINK_CTL = 0x01

OCF_LE_SET_SCAN_PARAMETERS = 0x000B
OCF_LE_SET_SCAN_ENABLE = 0x000C
OCF_LE_CREATE_CONN = 0x000D
OCF_LE_SET_ADVERTISING_PARAMETERS = 0x0006
OCF_LE_SET_ADVERTISE_ENABLE = 0x000A
OCF_LE_SET_ADVERTISING_DATA = 0x0008
OCF_LE_SET_SCAN_RESPONSE_DATA = 0x0009
OCF_DISCONNECT = 0x0006

LE_SET_SCAN_PARAMETERS_CMD = OCF_LE_SET_SCAN_PARAMETERS | OGF_LE_CTL << 10
LE_SET_SCAN_ENABLE_CMD = OCF_LE_SET_SCAN_ENABLE | OGF_LE_CTL << 10
LE_SET_ADVERTISING_PARAMETERS_CMD = OCF_LE_SET_ADVERTISING_PARAMETERS | OGF_LE_CTL << 10
LE_SET_ADVERTISING_DATA_CMD = OCF_LE_SET_ADVERTISING_DATA | OGF_LE_CTL << 10
LE_SET_SCAN_RESPONSE_DATA_CMD = OCF_LE_SET_SCAN_RESPONSE_DATA | OGF_LE_CTL << 10
LE_SET_ADVERTISE_ENABLE_CMD = OCF_LE_SET_ADVERTISE_ENABLE | OGF_LE_CTL << 10

LE_CREATE_CONN_CMD = OCF_LE_CREATE_CONN | OGF_LE_CTL << 10
DISCONNECT_CMD = OCF_DISCONNECT | OGF_LINK_CTL << 10



# Generic Access Profile
# BT Spec V4.0, Volume 3, Part C, Section 18

# https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile


"""
0x01	«Flags»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.3 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.3 and 18.1 (v4.0)Core Specification Supplement, Part A, section 1.3
0x02	«Incomplete List of 16-bit Service Class UUIDs»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.1 and 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
0x03	«Complete List of 16-bit Service Class UUIDs»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.1 and 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
0x04	«Incomplete List of 32-bit Service Class UUIDs»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, section 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
0x05	«Complete List of 32-bit Service Class UUIDs»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, section 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
0x06	«Incomplete List of 128-bit Service Class UUIDs»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.1 and 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
0x07	«Complete List of 128-bit Service Class UUIDs»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.1 and 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
0x08	«Shortened Local Name»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.2 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.2 and 18.4 (v4.0)Core Specification Supplement, Part A, section 1.2
0x09	«Complete Local Name»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.2 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.2 and 18.4 (v4.0)Core Specification Supplement, Part A, section 1.2
0x0A	«Tx Power Level»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.5 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.5 and 18.3 (v4.0)Core Specification Supplement, Part A, section 1.5
0x0D	«Class of Device»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.6 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.5 and 18.5 (v4.0)Core Specification Supplement, Part A, section 1.6
0x0E	«Simple Pairing Hash C»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.6 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.5 and 18.5 (v4.0)
0x0E	«Simple Pairing Hash C-192»	Core Specification Supplement, Part A, section 1.6
0x0F	«Simple Pairing Randomizer R»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.6 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.5 and 18.5 (v4.0)
0x0F	«Simple Pairing Randomizer R-192»	Core Specification Supplement, Part A, section 1.6
0x10	«Device ID»	Device ID Profile v1.3 or later
0x10	«Security Manager TK Value»	Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.7 and 18.6 (v4.0)Core Specification Supplement, Part A, section 1.8
0x11	«Security Manager Out of Band Flags»	Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.6 and 18.7 (v4.0)Core Specification Supplement, Part A, section 1.7
0x12	«Slave Connection Interval Range»	Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.8 and 18.8 (v4.0)Core Specification Supplement, Part A, section 1.9
0x14	«List of 16-bit Service Solicitation UUIDs»	Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.9 and 18.9 (v4.0)Core Specification Supplement, Part A, section 1.10
0x15	«List of 128-bit Service Solicitation UUIDs»	Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.9 and 18.9 (v4.0)Core Specification Supplement, Part A, section 1.10
0x16	«Service Data»	Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.10 and 18.10 (v4.0)
0x16	«Service Data - 16-bit UUID»	Core Specification Supplement, Part A, section 1.11
0x17	«Public Target Address»	Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.13
0x18	«Random Target Address»	Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.14
0x19	«Appearance»	Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.12
0x1A	«Advertising Interval»	Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.15
0x1B	«LE Bluetooth Device Address»	Core Specification Supplement, Part A, section 1.16
0x1C	«LE Role»	Core Specification Supplement, Part A, section 1.17
0x1D	«Simple Pairing Hash C-256»	Core Specification Supplement, Part A, section 1.6
0x1E	«Simple Pairing Randomizer R-256»	Core Specification Supplement, Part A, section 1.6
0x1F	«List of 32-bit Service Solicitation UUIDs»	Core Specification Supplement, Part A, section 1.10
0x20	«Service Data - 32-bit UUID»	Core Specification Supplement, Part A, section 1.11
0x21	«Service Data - 128-bit UUID»	Core Specification Supplement, Part A, section 1.11
0x22	«LE Secure Connections Confirmation Value»	Core Specification Supplement Part A, Section 1.6
0x23	«LE Secure Connections Random Value»	Core Specification Supplement Part A, Section 1.6
0x24	«URI»	Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.18
0x25	«Indoor Positioning»	Indoor Posiioning Service v1.0 or later
0x26	«Transport Discovery Data»	Transport Discovery Service v1.0 or later
0x27	«LE Supported Features»	Core Specification Supplement, Part A, Section 1.19
0x28	«Channel Map Update Indication»	Core Specification Supplement, Part A, Section 1.20
0x29	«PB-ADV»
Mesh Profile Specification Section 5.2.1
0x2A	«Mesh Message»
Mesh Profile Specification Section 3.3.1
0x2B	«Mesh Beacon»
Mesh Profile Specification Section 3.9
0x3D	«3D Information Data»	3D Synchronization Profile, v1.0 or later
0xFF	«Manufacturer Specific Data»	Bluetooth Core Specification:Vol. 3, Part C, section 8.1.4 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.4 and 18.11 (v4.0)Core Specification Supplement, Part A, section 1.4"""

GAP_FLAGS = 0x01
GAP_UUID_16BIT_INCOMPLETE = 0x02
GAP_UUID_16BIT_COMPLETE = 0x03
GAP_UUID_32BIT_INCOMPLETE = 0x04
GAP_UUID_32BIT_COMPLETE = 0x05
GAP_UUID_128BIT_INCOMPLETE = 0x06
GAP_UUID_128BIT_COMPLETE = 0x07
GAP_NAME_INCOMPLETE = 0x08
GAP_NAME_COMPLETE = 0x09
GAP_TX_POWER = 0x0A
# GAP_ = 0x0B   # UNUSED
# GAP_ = 0x0C   # UNUSED
GAP_DEVICE_CLASS = 0x0D
GAP_SIMPLE_PAIRING_HASH = 0x0E      # C or C-192
GAP_SIMPLE_PAIRING_RANDOMIZER = 0x0F    # R or R-192
GAP_DEVICE_ID = 0x10    # Not Unique: GAP_DEVICE_ID or GAP_SECURITY_MGR_TK_VALUE
GAP_SECURITY_MGR_OOBand_FLAGS = 0x11
GAP_SLAVE_CONNECTION_INTERVAL_RANGE = 0x12
#  = 0x13   # UNUSED
GAP_LIST_16BIT_SOLICITATION_UUID = 0x14
GAP_LIST_128BIT_SOLICITATION_UUID = 0x15
GAP_SERVICE_DATA = 0x16
GAP_PUBLIC_TARGET_ADDRESS = 0x17
GAP_RANDOM_TARGET_ADDRESS = 0x18
GAP_APPEARANCE = 0x19
GAP_ADVERTISING_INTERVAL = 0x1A
GAP_LE_BLUETOOTH_DEVICE_ADDRESS = 0x1B
GAP_LE_ROLE = 0x1C
GAP_SIMPLE_PAIRING_HASH_C256 = 0x1D
GAP_SIMPLE_PAIRING_RANDOMIZER_R256 = 0x1E
GAP_LIST_32BIT_SOLICITATION_UUID= 0x1F
GAP_SERVICE_DATA_32BIT_UUID = 0x20
GAP_SERVICE_DATA_128BIT_UUID = 0x21
GAP_SECURE_CONN_CONFIRMATION_VAL = 0x22
GAP_SECURE_CONN_RANDOM_VAL = 0x23
GAP_URI = 0x24
GAP_INDOOR_POSITIONING = 0x25
GAP_TRANS_DISC_DATA = 0x26
GAP_LE_SUPPORTED_FEATURES = 0x27
GAP_CHANNEL_MAP_UPDATE_IND = 0x28
GAP_PB_ADV = 0x29
GAP_MESH_MESSAGE = 0x2A
GAP_MESH_BEACON = 0x2B
GAP_BIG_INFO = 0x2C
GAP_BROADCAST_CODE = 0x2D
GAP_3D_INFO_DATA = 0x3D
GAP_MFG_DATA = 0xFF



# see: https://github.com/ARMmbed/ble/blob/8d97fced5440d78c9557693b6d1632f1ab5d77b7/ble/GapAdvertisingData.h

LE_LIMITED_DISCOVERABLE = 0x01 #, /**< Peripheral device is discoverable for a limited period of time. */
LE_GENERAL_DISCOVERABLE = 0x02 #, /**< Peripheral device is discoverable at any moment. */
BREDR_NOT_SUPPORTED     = 0x04 #, /**< Peripheral device is LE only. */
SIMULTANEOUS_LE_BREDR_C = 0x08 #, /**< Not relevant - central mode only. */
SIMULTANEOUS_LE_BREDR_H = 0x10 # /**< Not relevant - central mode only. */


# https://github.com/ARMmbed/ble/blob/8d97fced5440d78c9557693b6d1632f1ab5d77b7/ble/GapAdvertisingData.h



HCI_LE_META_EVENT = 0x3e

HCI_LE_META_EVENTS = {
        0x01 : "LE_Connection_Complete",
        0x02 : "LE_Advertising_Report",
        0x03 : "LE_Connection_Update_Complete",
        0x04 : "LE_Read_Remote_Used_Features_Complete",
        0x05 : "LE_Long_Term_Key_Request",
        0x06 : "LE_Remote_Connection_Parameter_Request"
    }


HCI_EVENTS = {
        0x01 : "Inquiry_Complete",
        0x02 : "Inquiry_Result",
        0x03 : "Connection_Complete",
        0x04 : "Connection_Request",
        0x05 : "Disconnection_Complete",
        0x06 : "Authentication_Complete",
        0x07 : "Remote_Name_Request_Complete",
        0x08 : "Encryption_Change",
        0x09 : "Change_Connection_Link_Key_Complete",
        0x0a : "Master_Link_Key_Complete",
        0x0b : "Read_Remote_Supported_Features_Complete",
        0x0c : "Read_Remote_Version_Information_Complete",
        0x0d : "QoS_Setup_Complete",
        0x0e : "Command_Complete",
        0x0f : "Command_Status",
        0x10 : "Hardware_Error",
        0x11 : "Flush_Occurred",
        0x12 : "Role_Change",
        0x13 : "Number_Of_Completed_Packets",
        0x14 : "Mode_Change",
        0x15 : "Return_Link_Keys",
        0x16 : "PIN_Code_Request",
        0x17 : "Link_Key_Request",
        0x18 : "Link_Key_Notification",
        0x19 : "Loopback_Command",
        0x1a : "Data_Buffer_Overflow",
        0x1b : "Max_Slots_Change",
        0x1c : "Read_Clock_Offset_Complete",
        0x1d : "Connection_Packet_Type_Changed",
        0x1e : "QoS_Violation",
        0x20 : "Page_Scan_Repetition_Mode_Change",
        0x21 : "Flow_Specification_Complete",
        0x22 : "Inquiry_Result_with_RSSI",
        0x23 : "Read_Remote_Extended_Features_Complete",
        0x2c : "Synchronous_Connection_Complete",
        0x2d : "Synchronous_Connection_Changed",
        0x2e : "Sniff_Subrating",
        0x2f : "Extended_Inquiry_Result",
        0x30 : "Encryption_Key_Refresh_Complete",
        0x31 : "IO_Capability_Request",
        0x32 : "IO_Capability_Response",
        0x33 : "User_Confirmation_Request",
        0x34 : "User_Passkey_Request",
        0x35 : "Remote_OOB_Data_Request",
        0x36 : "Simple_Pairing_Complete",
        0x38 : "Link_Supervision_Timeout_Changed",
        0x39 : "Enhanced_Flush_Complete",
        0x3b : "User_Passkey_Notification",
        0x3c : "Keypress_Notification",
        0x3d : "Remote_Host_Supported_Features_Notification",
        HCI_LE_META_EVENT : "LE_Meta_Event",
        0x40 : "Physical_Link_Complete",
        0x41 : "Channel_Selected",
        0x42 : "Disconnection_Physical_Link_Complete",
        0x43 : "Physical_Link_Loss_Early_Warning",
        0x44 : "Physical_Link_Recovery",
        0x45 : "Logical_Link_Complete",
        0x46 : "Disconnection_Logical_Link_Complete",
        0x47 : "Flow_Spec_Modify_Complete",
        0x48 : "Number_Of_Completed_Data_Blocks",
        0x4c : "Short_Range_Mode_Change_Complete",
        0x4d : "AMP_Status_Change",
        0x49 : "AMP_Start_Test",
        0x4a : "AMP_Test_End",
        0x4b : "AMP_Receiver_Report",
        0x4e : "Triggered_Clock_Capture",
        0x4f : "Synchronization_Train_Complete",
        0x50 : "Synchronization_Train_Received",
        0x51 : "Connectionless_Slave_Broadcast_Receive",
        0x52 : "Connectionless_Slave_Broadcast_Timeout",
        0x53 : "Truncated_Page_Complete",
        0x54 : "Slave_Page_Response_Timeout",
        0x55 : "Connectionless_Slave_Broadcast_Channel_Map_Change",
        0x56 : "Inquiry_Response_Notification",
        0x57 : "Authenticated_Payload_Timeout_Expired",
    }
