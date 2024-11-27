from Bio import Entrez
from pdfreader import SimplePDFViewer, PageDoesNotExist
import re
import requests

# 1. Pedir archivo PDF
print("Escribe la ruta del archivo: ")
print("Leyendo el archivo...")
pdf_file = open('C:/Users/danig/OneDrive/Documentos/INMEGEN/Genomind_AdrianaVega.pdf', "rb")
viewer = SimplePDFViewer(pdf_file)
images = []
strings = []
try:
    while True:
        viewer.render()
        images.extend(viewer.canvas.inline_images)
        images.extend(viewer.canvas.images.values())
        strings.extend(viewer.canvas.strings)
        viewer.next()
except PageDoesNotExist:
    pass

text = "".join(strings)

# 2. Buscar cadena de texto
patron = "rs\d+"
busqueda = re.findall(patron, text)
print("Lista de rs en el archivo: ", busqueda)

# 3. Buscar rs
Entrez.email = 'dgoretti@lcg.unam.mx'

'''
# Ejemplo
rs="rs2032583"

handle = Entrez.esearch(db="snp", term=rs)
record5 = Entrez.read(handle)
print("Datos base de rs: ", record5)

handle = Entrez.esummary(db="snp", id=record5["IdList"][0])
record6 = Entrez.read(handle)
print("SNP freq: ", record6)

try:
    while True:
        handle = Entrez.esearch(db="clinvar", term=rs)
        record2 = Entrez.read(handle)
        print("Clinvar: ", record2)
        handle = Entrez.esummary(db="clinvar", id=record2["IdList"][0])
        record4 = Entrez.read(handle)
        pharm_id = record4['DocumentSummarySet']['DocumentSummary'][0]['variation_set'][0]['variation_xrefs'][0][
            'db_id']
        
        handle = Entrez.esearch(db="snp", term=rs)
        record = Entrez.read(handle)
        handle = Entrez.efetch(db="snp", id=record["IdList"][0], rettype="docset", retmode="text")
        print("Frecuencia: ", handle.readline().strip())
        handle.close()

        var_url2 = "https://api.pharmgkb.org/v1/data/clinicalAnnotation/"
        response3 = requests.get(var_url2, [("id", pharm_id), ("view", "max")])
        print("Fenotipos: ", response3.json())

except IndexError:
    pass
'''



# 4. Hacer loop
for rs in busqueda:
    try:
        print("Nombre de rs: ", rs)
        handle = Entrez.esearch(db="snp", term=rs)
        record = Entrez.read(handle)
        print("rs data: ", record)

        handle = Entrez.esummary(db="snp", id=record["IdList"][0])
        record2 = Entrez.read(handle)
        print("Datos completos rs: ", record2)
        print("SNP freq: ", record2['DocumentSummarySet']['DocumentSummary'][0]['GLOBAL_MAFS'])

        handle = Entrez.esearch(db="gene", term=rs)
        record1 = Entrez.read(handle)
        handle = Entrez.esummary(db="gene", id=record1["IdList"][0])
        recordgene = Entrez.read(handle)
        print("Gene: ", recordgene['DocumentSummarySet']['DocumentSummary'])


        handle = Entrez.esearch(db="clinvar", term=rs)
        record3 = Entrez.read(handle)
        print("Clinvar ID: ", record3['IdList'][0])

        handle = Entrez.esummary(db="clinvar", id=record3["IdList"][0])
        record4 = Entrez.read(handle)
        print("Germline: ", record4)
        #print("Germline: ", record4['DocumentSummarySet']['DocumentSummary'][0]['germline_classification'])
        pharm_id = record4['DocumentSummarySet']['DocumentSummary'][0]['variation_set'][0]['variation_xrefs'][0][
            'db_id']

        var_url2 = "https://api.pharmgkb.org/v1/data/clinicalAnnotation/"
        response3 = requests.get(var_url2, [("id", pharm_id), ("view", "max")])
        print("Fenotipos: ", response3.json())

    except IndexError:
        pass
