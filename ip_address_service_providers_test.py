import sys
import unittest

import ip_address_service_providers as service

EXPECT_IP = 'unspecified ip address'


class IPAddressServiceProvider(unittest.TestCase):

  def setUp(self):
    self.providers = (
        service.AmazonAWSService(),
        service.DynDNSService(),
        service.IfConfigService(),
        service.CorzService())

  def test_get_ip(self):
    for provider in self.providers:
      self.assertEqual(EXPECT_IP, provider.get_ip())


if __name__ == '__main__':
  # TODO: improve this manual setting.
  if len(sys.argv) == 2:
    EXPECT_IP = sys.argv.pop(-1)
    unittest.main()
  else:
    print (
        'Test usage:\n'
        'python ip_address_service_providers_test.py ${expect_ip}')
