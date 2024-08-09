import json
import base64
import urllib
import httplib
from Autodesk.DesignScript.Geometry import *
import clr
import sys
sys.path.append('C:\Program Files (x86)\IronPython 2.7\Lib')

clr.AddReference('ProtoGeometry')
# The inputs to this node will be stored as a list in the IN variables.
url = IN[0]
db = IN[1]
user = IN[2]
password = IN[3]
query = """PREFIX : <http://example.org/fagerhult_notor_product_data#>
        PREFIX notor: <http://example.org/fagerhult_notor_ontology#>
        SELECT * WHERE{ 
                ?notor a notor:A1_LD_Notor65_Betaopti.
                ?notor :hasArtNr ?ArtNr.         
            }"""
reasoning = IN[5]
go = IN[6]

if go:

    # Defaults
    if not reasoning:
        reasoning = False

    # DB CONNECTION

    # Establish connection
    conn = httplib.HTTPConnection(url)

    # Encode username and password in base64
    encodedAuth = base64.b64encode('%s:%s' % (user, password))

    # Define headers for authorizatio etc.
    headers = {"authorization": ("Basic %s" % encodedAuth),
               "Content-type": "application/x-www-form-urlencoded", "Accept": "application/sparql-results+json"}

    # Define parameters (qyery, reasoning etc.)
    params = urllib.urlencode({"query": query, "reasoning": reasoning})

    # Send request
    conn.request('GET', '/' + db + '/query', params, headers)

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
