# 1. Abrir librerias
from pdfreader import SimplePDFViewer
from PyPDF2 import PdfReader
import re

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

if industry == "Genomind":
    start_page = 3
    final_page = 7
    for page in range(start_page, final_page):
        viewer.navigate(page)
        viewer.render()
        plain_text += "".join(viewer.canvas.strings)
        viewer.next()
elif industry == "Oneome":
    start_page = 11
    final_page = 15
    for page in range(start_page, final_page):
        viewer.navigate(page)
        viewer.render()
        plain_text += "".join(viewer.canvas.strings)
        viewer.next()
elif industry == "Novogenia":
    plain_full = ""
    PDF_read = PdfReader(pdf_file)
    for page in range(13, 16):
        pages = PDF_read.pages[page]  # 13 a 15
        plain_full += ''.join(pages.extract_text())
    plano = " ".join(plain_full.split())
    plain_text = plano.replace(' ', '')

print(plain_text)

# 2. Lista de genes de importancia clínica en salud mental
genes = ["ABCB1", "ADRA2A", "5HT2C", "HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1",
         "CYP3A4", "CYP3A5", "COMT", "DRD2", "GRIK1", "GRIK4", "HLA-A", "HLA-B", "HTR2A", "MC4R", "MTHFR", "NAT2",
         "OPRM1", "SLC6A4", "TPMT", "UGT1A1", "UGT1A4", "UGT2B15"]
print("Lista de genes en el archivo: ", genes)

# Genomind: variantes pegadas
# Oneome: variantes pegadas
# Novogenia:

# 5. Buscar genes y genotipos * en archivos
genotipos = []
found = []
wo_extensive1 = plain_text.split('EXTENSIVE')

# Eliminar genotipos repetidos
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
        patron = g + r"\w+\/\w+"
        busqueda1 = re.findall(patron, plain_text)
        if len(busqueda1) != 0:
            genotipos.extend(busqueda1)
        patron2 = g + r"\w+[/*(:)]+\w+"
        busqueda2 = re.findall(patron2, plain_text)
        if len(busqueda2) != 0:
            genotipos.extend(busqueda2)

        print(busqueda2)
        # print(busqueda1)

# Eliminar genotipos repetidos
    genotipos_unicos1 = []
    for genotipo in genotipos:
        if genotipo not in genotipos_unicos1:
            genotipos_unicos1.append(genotipo)
    genotipos_unicos = []
    for geno in genotipos_unicos1:
        patron4 = r'\DM'
        correc = re.sub(patron4, "", geno)
        genotipos_unicos.append(correc)
    print("Genotipos unicos: ", genotipos_unicos)
