# PROGRAMA PARA DETECTAR VARIANTES FARMACOGENÓMICAS RELACIONADAS CON MEDICAMENTOS PSIQUIATRICOS
# 1. Abrir librerias
from Bio import Entrez
from pdfreader import SimplePDFViewer, PageDoesNotExist
import re
import requests

# 2. Abrir archivos PDF
print("Escriba la industria a la que pertenecen sus resultados (Oneome, Genomind, Novogenia)")
industry = input()
print("Escriba la ruta del archivo PDF: ")
# RUTAS
# a) 'C:/Users/danig/OneDrive/Documentos/INMEGEN/Genomind_AdrianaVega.pdf'
# b) 'C:/Users/danig/Downloads/M8I9347-REPORT-SofiaJastrow.pdf'
# c) 'C:/Users/danig/Downloads/oneome-report-A4E01.pdf'

pdf_file = open(input(), "rb")
viewer = SimplePDFViewer(pdf_file)

plain_text = ""

try:
    while True:
        viewer.render()
        plain_text += "".join(viewer.canvas.strings)
        viewer.next()
except PageDoesNotExist:
    pass

print(plain_text)

# 2. Lista de genes de importancia clínica en salud mental
genes = ["ABCB1", "ADRA2A", "5HT2C/HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1",
         "CYP3A4", "CYP3A5", "COMT", "DRD2", "GRIK1", "GRIK4", "HLA-A", "HLA-B", "HTR2A", "MC4R", "MTHFR", "NAT2",
         "OPRM1", "SCL6A4", "TPMT", "UGT1A1", "UGT1A4", "UGT2B15"]

# Genomind: variantes pegadas
# Oneome: variantes pegadas
# Novogenia:

# 3. Buscar genes y genotipos * en archivos

print("Lista de genes en el archivo: ")
genotipos = []

for g in genes:
    patron = g + "\W\d+\W+\d+"
    busqueda1 = re.findall(patron, plain_text)
    if len(busqueda1)!=0:
        print("Opciones del gen", g, ": ", busqueda1)
        genotipos.append(busqueda1)
    patron2 = g + "\w+\W\w+"
    busqueda2 = re.findall(patron2, plain_text)
    if len(busqueda2)!= 0:
        print("Otras opciones: ", busqueda2)

print(genotipos)

# 4. Búsqueda de rs en archivos
patron = "rs\d+"
busqueda = re.findall(patron, plain_text)
print("Lista de rs en el archivo: ", busqueda)

# 5. Buscar rs y genotipos * en archivos
# Imprimir nombre de rs, los datos de snp del rs, la frecuencia en snp, el gen de donde proviene, buscar pharm_id y
# los fenotipos

Entrez.email = 'dgoretti@lcg.unam.mx'


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
        print("Germline: ", record4['DocumentSummarySet']['DocumentSummary'][0]['germline_classification'])
        pharm_id = record4['DocumentSummarySet']['DocumentSummary'][0]['variation_set'][0]['variation_xrefs'][0][
            'db_id']

        var_url2 = "https://api.pharmgkb.org/v1/data/clinicalAnnotation/"
        response3 = requests.get(var_url2, [("id", pharm_id), ("view", "max")])
        print("Fenotipos: ", response3.json())

    except IndexError:
        pass
