# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
from urllib.request import urlopen, Request

# The inputs to this node will be stored as a list in the IN variables.
url = IN[0]

# Place your code below this line

# Define the local filename to save data
local_file = 'C:\\Users\\kebreh\\Fagerhult\\\IES_downloads\\iesfile.ies'

# Define the URI of the download for the file to retrieve
remote_url = url


# Get the content of the URI
response = urlopen(
    Request(
        remote_url,
        headers={
            # Not needed to be specified.
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
    )
)

# Decode the content and write it to the local file.
with open(local_file, "w") as local_file:
    file_content = response.read().decode(
        'utf-8-sig')  # -sig to delete the BOM signature
    local_file.write(file_content)


# Assign your output to the OUT variable.
OUT = 'C:\\Users\\kebreh\\Fagerhult\\\IES_downloads\\iesfile.ies'