"""Base class for ip address quering service."""
import logging
import socket
import sys
import urllib2


class IPAddressService(object):
  """Ip address quering service base class.

  overwrite the name and host member for derived service.
  overwrite extract_ip method to parse the http body.
  """

  def __init__(self):
    # The name of the service, must be provided by derived class.
    self.name = None
    # The request address or object, must be provided by derived class.
    self.host = None
    self.set_logger()

  def set_logger(self):
    """Set up proper logging to stdout."""
    # TODO: implement the logger configuration.
    self.logger = logging.getLogger(self.name)
    self.logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    self.logger.addHandler(ch)

  def get_ip(self):
    """Get local machine's public ip address from ther service.

    Returns:
      a str of the ip address if successful, else None.
    """
    self.logger.info('Retrieving ip address from %s', self.host)
    try:
      result = urllib2.urlopen(self.host)
    except urllib2.HTTPError as err:
      self.logger.error('HTTPError %d: %s', err.code, err.reason)
    except urllib2.URLError as err:
      self.logger.error('URLError %d: %s', err.code, err.reason)
    else:
      if result.getcode() == 200:
        self.logger.info('Retrieved data from %s', self.host)
        return self.extract_ip(result.read())
      else:
        self.logger.error('Unknown HTTP status code %d', result.getcode())

  def extract_ip(self, http_body):
    """Extract the ipv4 address string from http reply body.

    Args:
      http_body: the body of http reply.
    Returns:
      the str representation of ipv4 address or None
    """
    return self.validate_ipv4(http_body.strip())

  def validate_ipv4(self, addr):
    """Validates an ipv4 address.

    Args:
      addr: the str of ipv4 address.
    Returns:
      the same str as input if it's valid or None if not.
    """
    try:
      socket.inet_aton(addr)
    except socket.error:
      # Not legal
      self.logger.error('Invalid IPv4 address recieved: %s', addr)
    else:
      # legal
      return addr
