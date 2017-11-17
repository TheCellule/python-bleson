import unittest

from bleson.core.types import UUID16, UUID128


class TestUUID(unittest.TestCase):

    def test_uuid16_init(self):
        u1 = UUID16(bytearray([0x0d, 0x1a]))
        u2 = UUID16(0x1a0d)

        self.assertEqual(0x1a0d, u1.uuid)
        self.assertEqual(0x1a0d, u2.uuid)
        self.assertEqual(u1, u2)

    def test_uuid128_init(self):
        u1 = UUID128([0x23, 0xD1, 0xBC, 0xEA, 0x5F, 0x78, 0x23, 0x15, 0xDE, 0xEF, 0x12, 0x12, 0x30, 0x15, 0x00, 0x00])
        u2 = UUID128('00001530-1212-efde-1523-785feabcd123')
        u3 = UUID128('12345678-1212-efde-1523-785feabcd123')
        u4 = UUID128(0xFEFF)
        self.assertEqual('00001530-1212-efde-1523-785feabcd123', u1.uuid)
        self.assertEqual('00001530-1212-efde-1523-785feabcd123', u2.uuid)
        self.assertEqual(u1, u2)
        self.assertNotEqual(u3, u1)
        self.assertNotEqual(u4, u1)
