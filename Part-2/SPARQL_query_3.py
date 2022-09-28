# Load the Python Standard and DesignScript Libraries
from urllib.parse import urlparse
import stardog
import json
from Autodesk.DesignScript.Geometry import *
import sys
import clr
clr.AddReference('ProtoGeometry')


# The inputs to this node will be stored as a list in the IN variables.
db = IN[0]
artnr_List = IN[1]
artnr = artnr_List[0]
ep = IN[2]


# specify stardog connection details
conn = stardog.Connection(
    db,  # database name
    endpoint=ep,
    username='admin',
    password='admin'
)

query_1 = """
PREFIX : <http://example.org/fagerhult_notor_product_data#> 
PREFIX notor: <http://example.org/fagerhult_notor_ontology#> 
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?property ?objectValue WHERE{
    ?notor :hasArtNr
    """

query_2 = """
         ?notor   ?property ?objectValue .                        
        } 
        """
query = query_1 + "'" + artnr + "'" + '.' + query_2

results_JSON = conn.select(
    query,
    content_type=stardog.content_types.SPARQL_JSON,
    bindings={'query': '"star AND dog"'}
)

results_property_value = results_JSON["results"]["bindings"]

prop_value = []

for i in results_property_value:
    parsed_url = urlparse(i["property"]["value"])
    # index 5: fragment of url
    prop_value.append(
        {"property": parsed_url[5], "value": i["objectValue"]["value"]})

# Assign your output to the OUT variable.
OUT = prop_value
