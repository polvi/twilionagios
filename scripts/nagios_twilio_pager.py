#!/usr/bin/env python

import twiliorest
import sys

# Twilio REST API version
API_VERSION = '2008-08-01'
ACCOUNT_SID = 'YOUR SID HERE'
ACCOUNT_TOKEN = 'YOUR TOKEN HERE'
# needs to be registered with twillo
CALLER_ID = 'YOUR-CALLER-ID';

# this needs point to where you run your "twistd twilio_nagios" instance
MONITOR_URL = 'http://localhost:8080'

# Create a Twilio REST account object using your Twilio account ID and token
account = twiliorest.Account(ACCOUNT_SID, ACCOUNT_TOKEN)

number = sys.argv[1]
type = sys.argv[2]
service = sys.argv[3]
host = sys.argv[4]

d = {
    'Caller' : CALLER_ID,
    'Called' : number,
    'Url' : '%s/%s/%s/%s' % (MONITOR_URL, type, service, host),
}
print account.request('/%s/Accounts/%s/Calls' % \
    (API_VERSION, ACCOUNT_SID), 'POST', d)
