
import xlrd
from rdflib.namespace import FOAF
from rdflib import URIRef, Graph, Literal, RDF, RDFS, Namespace
import re

# read the fagerhult product data excel file
product_data_excel_file = "C:/Users/kebreh/Fagerhult/Generate_Ontology/Notor65_betaopti.xlsx"
product_data_book = xlrd.open_workbook(product_data_excel_file)

# creat a triple store
store = Graph()
# bind a default prefix, namespace pairs for pretty output
default_ns = Namespace("http://example.org/fagerhult_notor_ontology#")
store.bind("", default_ns)
CEN_onto_ns = Namespace(
    "http://example.org/BIM_lighting_properties_standards/CEN_TC_274_Ontology#")
store.bind("cen", CEN_onto_ns)


# process the data in the sheet "Family"
sheet = product_data_book.sheet_by_name("Family")

# create a class "Notor" family
class_notor_family = URIRef(
    default_ns + sheet.cell_value(rowx=2, colx=1).strip())
store.add((class_notor_family, RDF.type, RDFS.Class))
# add the description to the class
store.add((class_notor_family, RDFS.comment, Literal(
    sheet.cell_value(rowx=3, colx=1).replace("<br>", " ").replace("\n", " "))))

# process the data in the sheet "Product"
sheet = product_data_book.sheet_by_name("Product")

# create a class "Notor 65 Beta Opti" Product
class_notor_product = URIRef(
    default_ns + sheet.cell_value(rowx=3, colx=3).strip().replace(" ", "_"))
store.add((class_notor_product, RDF.type, RDFS.Class))
store.add((class_notor_product, RDFS.subClassOf, class_notor_family))
# add the description to the class
# the value from the field "Product Preamble"), might need to be changed later!
store.add((class_notor_product, RDFS.comment,
          Literal(sheet.cell_value(rowx=4, colx=3))))


# process the data in the sheet "Item"
sheet = product_data_book.sheet_by_name("Item")
# create a class  "A1 LD Notor65 Betaopti" family produc subgroup
class_notor_product_item = URIRef(
    default_ns + sheet.cell_value(rowx=9, colx=3).strip().replace(" ", "_"))
store.add((class_notor_product_item, RDF.type, RDFS.Class))
store.add((class_notor_product_item, RDFS.subClassOf, class_notor_product))
# add the description to the class
# the value from the field "ItemJeevesDescription"), might need to be changed later!
store.add((class_notor_product_item, RDFS.comment,
          Literal(sheet.cell_value(rowx=7, colx=3))))


# read the mapping excel file
mapping_excel_file = "C:/Users/kebreh/Fagerhult/Generate_Ontology/mapping2standard.xlsx"
mapping_book = xlrd.open_workbook(mapping_excel_file)
mapping_sheet = mapping_book.sheet_by_index(0)
for row in mapping_sheet.get_rows():
    # At the moment we only handle the properties having mappings in the standards
    if row[4].value and row[0].value:
        # clean the name string
        name = re.sub('[^A-Za-z0-9]+', '_', row[0].value.strip())
        property_notor_item = URIRef(default_ns + name)
        store.add((property_notor_item, RDF.type, RDF.Property))
        store.add((property_notor_item, RDFS.range, class_notor_product_item))
        store.add((property_notor_item, RDFS.seeAlso,
                  URIRef(CEN_onto_ns + row[4].value.strip())))


# Serialize as Turtle
rdffile = open('fagerhult_notor_ontology.ttl', 'wb')
rdffile.write(store.serialize(format="turtle"))

rdffile.close()
