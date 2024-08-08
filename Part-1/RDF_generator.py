import xlrd
from rdflib.namespace import FOAF
from rdflib import URIRef, Graph, Literal, RDF, RDFS, Namespace
import re


# read the fagerhult product data excel file

product_data_excel_file = 'C:/Users/kebreh/Fagerhult/Generate_Ontology/Notor65_betaopti_RDF_TEN.xlsx'
product_data_book = xlrd.open_workbook(product_data_excel_file)

# creat a triple store
store = Graph()
# bind a default prefix, namespace pairs for pretty output
default_ns = Namespace("http://example.org/fagerhult_notor_product_data#")
store.bind("notor", default_ns)
fagerhult_notor_ontology_ns = Namespace(
    "http://example.org/fagerhult_notor_ontology#")
store.bind("", fagerhult_notor_ontology_ns)

# create a property for Art Nr
prop_art_nr = URIRef(default_ns + "hasArtNr")
store.add((prop_art_nr, RDF.type, RDF.Property))

# process the data in the sheet "All item"
sheet = product_data_book.sheet_by_name("All items")

# go through all the items
for i in range(3, sheet.ncols-1):
    # naming it using ENA
    item = URIRef(default_ns + sheet.cell_value(1, i).strip())
    store.add((item, RDF.type, URIRef(
        fagerhult_notor_ontology_ns + "A1_LD_Notor65_Betaopti")))
    store.add((item, prop_art_nr, Literal(sheet.cell_value(2, i).strip())))

    # go through all the properties
    for j in range(3, sheet.nrows-1):
        if(sheet.cell(j, i).value and sheet.cell(j, i).value != "NA"):
            name = re.sub('[^A-Za-z0-9]+', '_', sheet.cell_value(j, 0).strip())
            store.add((item, URIRef(fagerhult_notor_ontology_ns +
                                    name), Literal(sheet.cell_value(j, i))))


# Serialize as Turtle
rdffile = open('fagerhult_notor_product_data_20220112.ttl', 'wb')
rdffile.write(store.serialize(format="turtle"))

rdffile.close()
