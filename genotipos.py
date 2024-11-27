from Bio import Entrez
from pdfreader import SimplePDFViewer
from PyPDF2 import PdfReader
import re
import requests

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
PDF_read = PdfReader(pdf_file)
for page in range(13, 16):
    pages = PDF_read.pages[page]  # 13 a 15
    # print(pages.extract_text())
    plain_text += ''.join(pages.extract_text())

# print(strings)

# print(plain_text)
plano = " ".join(plain_text.split())
# print(plano)
plain_full = plano.replace(' ', '')
# print(plain_full)

genes = ["ABCB1", "ADRA2A", "5HT2C/HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1",
         "CYP3A4", "CYP3A5", "COMT", "DRD2", "GRIK1", "GRIK4", "HLA-A", "HLA-B", "HTR2A", "MC4R", "MTHFR", "NAT2",
         "OPRM1", "SCL6A4", "TPMT", "UGT1A1", "UGT1A4", "UGT2B15"]
print("Lista de genes en el archivo: ", genes)

Entrez.email = 'dgoretti@lcg.unam.mx'

genotipos = []
found = []
wo_extensive1 = plain_full.split('EXTENSIVE')

if industry == 'Novogenia':
    for gen in genes:
        for g in wo_extensive1:
            patron = gen + r'.+\*\w+\/\*\w{1,2}'
            busqueda3 = re.findall(patron, g)
            if len(busqueda3) != 0:
                genotipos.extend(busqueda3)
    # print(genotipos)

    genotipos_unicos = []

    for g in genotipos:
        patron3 = r'rs.+ACTIVIDAD'
        partes = re.sub(patron3, "", g)
        genotipos_unicos.append(partes)

    print(genotipos_unicos)

else: 
    for g in genes:
        patron = g + r"\W\d+\W+\d+"
        busqueda1 = re.findall(patron, plano)
        if len(busqueda1) != 0:
            genotipos.extend(busqueda1)
        patron2 = g + r"\w+\W\w+"
        busqueda2 = re.findall(patron2, plano)
        if len(busqueda2) != 0:
            genotipos.extend(busqueda2)

# Eliminar genotipos repetidos
    genotipos_unicos = []
    for genotipo in genotipos:
        if genotipo not in genotipos_unicos:
            genotipos_unicos.append(genotipo)

    print("Genotipos unicos (", len(genotipos_unicos), "): ", genotipos_unicos)
