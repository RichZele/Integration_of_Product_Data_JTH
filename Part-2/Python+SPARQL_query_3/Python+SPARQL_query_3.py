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
prop_value = IN[1]
ep = IN[2]

# specify stardog connection details
conn = stardog.Connection(
    # database name - comes as input (IN) in dynamo
    db,
    endpoint=ep,
    username='admin',
    password='admin'
)

list_of_properties = []
# iterate over the list
for i in prop_value:
    # i is a dict
    # get the values of the keys with the key name
    list_of_properties.append(i.get('property'))
# print(list_of_properties)


translated_list = []
for prop in list_of_properties:
    # run a SPARQL query for each property (prop) to get its standard name
    query_1 = """
            prefix : <http://example.org/fagerhult_notor_ontology#> 
            prefix notor: <http://example.org/fagerhult_notor_product_data#> 
            prefix cen: <http://example.org/BIM_lighting_properties_standards/CEN_TC_274_Ontology#> 
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT  ?cenName WHERE{
                :"""
    query_2 = """ rdfs:seeAlso ?cenName .                                  
            } 
            """
    query = query_1 + prop + query_2

    prop_JSON = conn.select(
        query,
        content_type=stardog.content_types.SPARQL_JSON,
        bindings={'query': '"star AND dog"'}
    )

    property_name = prop_JSON["results"]["bindings"]

    for i in property_name:
        parsed_url = urlparse(i["cenName"]["value"])
        translated_list.append(parsed_url[5])

# Assign your output to the OUT variable.
OUT = translated_list
