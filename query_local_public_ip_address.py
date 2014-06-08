"""An application to find the public ip address of the local machine."""
import collections
from multiprocessing import Process, Queue
import sys

import ip_address_service_providers as service


def queue_ip_address(queue, service):
  """Use a service to get the ip address and put it in the queue.

  Args:
    queue: a multiprocessing.Queue instance for queried result (name, ip)
    service: an ip address service instance
  """
  queue.put((service.name, service.get_ip()))


def get_reconcile_ip_address(ip_addresses, size):
  """Get reconciled ip address.

  Args:
    ip_addresses: a multiprocessing.Queue for queried result(name, ip).
    size: an int of maximum queue size.
  Returned:
    (str, list) a str of the ip address and a list of providers, or
    (None, None) if there's no address agreed by at least 2 providers.
  """
  # holder for the ip addresses we are going to reconcile.
  result = collections.defaultdict(list)

  while size:
    name, ip = ip_addresses.get()
    result[ip].append(name)
    if ip and len(result[ip]) > 1:
      # We have an ip address with 2 services agreed.
      return ip, result[ip]
    size -= 1
  return None, None


def main():
  # Add the ip querying services we have here.
  providers = (
      service.AmazonAWSService(),
      service.DynDNSService(),
      service.IfConfigService(),
      service.CorzService())

  # Queue for the queried ip addresses.
  ip_addresses = Queue()

  # List of processes we are running
  processes = []
  for provider in providers:
    p = Process(target=queue_ip_address, args=(ip_addresses, provider))
    p.start()
    processes.append(p)

  ip, services = get_reconcile_ip_address(ip_addresses, len(processes))
  for p in processes:
    if p.is_alive():
      p.terminate()

  if ip:
    print (
        'The local machine\'s public ip address is:\n'
        '%s\nConfirmed by:\n%s\n%s' % (ip, services[0], services[1]))
  else:
    # All the processes either failed or return different results.
    print 'No confirmed ip address'

if __name__ == '__main__':
  if len(sys.argv) > 1:
    print 'Not accepting parameters for this application'
  else:
    main()
