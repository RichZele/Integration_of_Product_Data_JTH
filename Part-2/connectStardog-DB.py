import json
import base64
import urllib
import httplib
from urllib2 import Request, urlopen
import clr
import sys
sys.path.append('C:\Program Files (x86)\IronPython 2.7\Lib')


# The inputs to this node will be stored as a list in the IN variables.
url = IN[0]
user = IN[1]
password = IN[2]
go = IN[3]

if go:

    # DB CONNECTION

    # Establish connection
    conn = httplib.HTTPConnection(url)

    # Encode username and password in base64
    encodedAuth = base64.b64encode('%s:%s' % (user, password))

    # Define headers for authorizatio etc.
    headers = {"authorization": ("Basic %s" % encodedAuth)}

    # Define parameters (qyery, reasoning etc.)
    params = urllib.urlencode({})

    # Send request
    conn.request('GET', '/admin/databases', params, headers)

    # Get response
    response = conn.getresponse()

    # Read response
    data = response.read()

    # Close db connection
    conn.close()

else:
    data = 'off mode'

# Assign your output to the OUT variable.
OUT = data
