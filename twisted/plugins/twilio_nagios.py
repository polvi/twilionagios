from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.web import server
from twisted.python import usage

from twilionagios import TwilioNagios

class Options(usage.Options):
  optParameters = [['port', 'p', 8080, 'port to run the twilio responder on'],
                   ['objects', 'o', '/var/cache/nagios3/objects.cache', 'location of nagios object cache'],
                   ['status', 's', '/var/cache/nagios3/status.dat', 'location of the nagios status data file']
                  ]

class ServiceMaker(object):
  implements(IServiceMaker, IPlugin)
  tapname = 'twilio_nagios'
  description = 'a nagios status parser that returns the data in twilio xml format'
  options = Options

  def makeService(self, options):
    site = server.Site(TwilioNagios(options['objects'], options['status']))
    return internet.TCPServer(int(options['port']),site)

serviceMaker = ServiceMaker()
