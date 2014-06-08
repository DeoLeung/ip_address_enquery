"""
1. http://checkip.amazonaws.com/
2. http://checkip.dyndns.org/
3. http://ifconfig.me/ip
4. http://corz.org/ip
"""
from ip_address_service import IPAddressService as ip
import re
import urllib2

class AmazonAWSService(ip):

  def __init__(self):
    self.name = 'Amazon AWS IP Address Service'
    self.host = 'http://checkip.amazonaws.com/'
    self.set_logger()


class DynDNSService(ip):

  def __init__(self):
    self.name = 'Dyn DNS IP Address Service'
    self.host = 'http://checkip.dyndns.org/'
    self.body_regex = re.compile('<body>Current IP Address: (.*)</body>')
    self.set_logger()

  def extract_ip(self, http_body):
    """Current IP Address: 31.51.59.26"""
    groups = self.body_regex.search(http_body)
    if groups:
      ip_string = groups.group(1)
    else:
      ip_string = http_body
    return self.validate_ipv4(ip_string)


class IfConfigService(ip):

  def __init__(self):
    self.name = 'If Config IP Address Service'
    self.host = 'http://ifconfig.me/ip'
    self.set_logger()


class CorzService(ip):

  def __init__(self):
    self.name = 'Corz IP Address Service'
    self.host = urllib2.Request(
        url='http://corz.org/ip',
        headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) '
                               'Gecko/20071127 Firefox/2.0.0.11'})
    self.set_logger()
