#!/usr/bin/python
from twisted.web.resource import Resource

import re

def parse_objects(file):
  filename = file
  conf = []
  f = open(filename, 'r')
  for i in f.readlines():
      if i[0] == '#': continue
      matchID = re.search(r"define ([\w]+) {", i)
      matchAttr = re.search(r"[ ]*([\w]+)\s+(.*)$", i)
      matchEndID = re.search(r"[ ]*}", i)
      if matchID:
          identifier = matchID.group(1)
          cur = [identifier, {}]
      elif matchAttr:
          attribute = matchAttr.group(1)
          value = matchAttr.group(2)
          cur[1][attribute] = value
      elif matchEndID:
          conf.append(cur)
  new_conf = {}
  for entry in conf:
    if entry[0] == 'host':
      new_conf[('host', entry[1]['host_name'])] = entry[1]
    elif entry[0] == 'service':
      new_conf[(entry[1]['service_description'], entry[1]['host_name'])] = entry[1]
  return new_conf

def parse_status(file):
  filename = file
  conf = []
  f = open(filename, 'r')
  for i in f.readlines():
      if i[0] == '#': continue
      matchID = re.search(r"([\w]+) {", i)
      matchAttr = re.search(r"[ ]*([\w]+)=([\w\d]*)", i)
      matchEndID = re.search(r"[ ]*}", i)
      if matchID:
          identifier = matchID.group(1)
          cur = [identifier, {}]
      elif matchAttr:
          attribute = matchAttr.group(1)
          value = matchAttr.group(2)
          cur[1][attribute] = value
      elif matchEndID:
          conf.append(cur)
  new_conf = {}
  for entry in conf:
    if entry[0] == 'hoststatus':
      new_conf[('host', entry[1]['host_name'])] = entry[1]
    elif entry[0] == 'servicestatus':
      new_conf[(entry[1]['service_description'], entry[1]['host_name'])] = entry[1]
  return new_conf

HOST_STATE_MSG = {
  0: 'up',
  1: 'down',
  2: 'unreachable'
}
SERVICE_STATE_MSG = {
  0: 'ok',
  1: 'warning',
  2: 'critical',
  3: 'unknown'
}
class TwilioNagios(Resource):
  isLeaf = True

  def __init__(self, objects, status):
    self.objects = objects
    self.status = status
    
  def render(self, request):
    request.setHeader( 'Content-Type', 'text/xml' )
    status = parse_status(self.status)
    conf = parse_objects(self.objects)
    try:
      type, service, name = request.postpath
      status_data = status[(service,name)]
      host_data = conf[('host',name)]
    except (KeyError, ValueError):
      return '<Response/>'

    state = int(status_data['current_state'])
    if type == 'service':
      say = 'service %s on host %s is %s' % \
        (service, 
         host_data['alias'], 
         SERVICE_STATE_MSG[state])

    msg = host_data.get('notes', host_data['alias'])
    if type == 'host':
      if state == 1:
        say = 'host %s is %s, I repeat, the host %s is %s' % \
          (msg, 
           HOST_STATE_MSG[state],
           msg,
           HOST_STATE_MSG[state])
      else:
        say = 'the host %s is %s' % \
          (msg,
           HOST_STATE_MSG[state])

    response = """
<Response>
  <Say>%s</Say>
</Response> """ % (say) #(data['long_plugin_output'])
    return response
