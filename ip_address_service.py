"""wrapper of Blizzard diablo3 web api."""
import logging
import socket
import sys
import urllib2


class IPAddressService(object):

  def __init__(self):
    self.name = None
    self.host = None
    self.set_logger()


  def set_logger(self):
    # TODO: implement the logger configuration.
    self.logger = logging.getLogger(self.name)
    self.logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    self.logger.addHandler(ch)

  def get_ip(self):
    self.logger.info('Retrieving ip address from %s', self.host)
    try:
      result = urllib2.urlopen(self.host)
    except urllib2.HTTPError as err:
      self.logger.error('HTTPError %d: %s', err.code, err.reason)
      return
    except urllib2.URLError as err:
      self.logger.error('URLError %d: %s', err.code, err.reason)
      return
    if result.getcode() == 200:
      self.logger.info('Retrieved data from %s', self.host)
      return self.extract_ip(result.read())
    else:
      self.logger.error('Unknown HTTP status code %d', result.getcode())

  def extract_ip(self, http_body):
    return self.validate_ipv4(http_body.strip())

  def validate_ipv4(self, addr):
    try:
      socket.inet_aton(addr)
    except socket.error:
      # Not legal
      self.logger.error('Invalid IPv4 address recieved: %s', addr)
    else:
      # legal
      return addr

