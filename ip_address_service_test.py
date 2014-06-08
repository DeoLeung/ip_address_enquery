import unittest

import ip_address_service


class IPAddressService(unittest.TestCase):

  def setUp(self):
    self.service = ip_address_service.IPAddressService()
    self.input_expect = (
        ('0.0.0.0', '0.0.0.0'),
        ('192.168.1.1', '192.168.1.1'),
        ('192.168.1.01', '192.168.1.01'),
        # TODO: depends on requirement we may not accept ipv4 with less than
        #       3 dots.
        ('192.168', '192.168'),
        ('13', '13'),
        ('efg', None),
        ('', None),)

  def test_validate_ipv4(self):
    for i, e in self.input_expect:
      self.assertEqual(e, self.service.validate_ipv4(i))

  def test_extract_ip(self):
    for i, e in self.input_expect:
      self.assertEqual(e, self.service.extract_ip(i))


if __name__ == '__main__':
  unittest.main()
