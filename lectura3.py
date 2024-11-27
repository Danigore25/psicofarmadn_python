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
    for page in range(2, 6):
        viewer.navigate(page)
        viewer.render()
        plain_text += "".join(viewer.canvas.strings)
elif industry == "Oneome":
    start_page = 11
    final_page = 15
    for page in range(start_page, final_page):
        viewer.navigate(page)
        viewer.render()
        plain_text += "".join(viewer.canvas.strings)
elif industry == "Novogenia":
    plain_full = ""
    PDF_read = PdfReader(pdf_file)
    for page in range(13, 16):
        pages = PDF_read.pages[page]  # 13 a 15
        plain_full += ''.join(pages.extract_text())
    plano = " ".join(plain_full.split())
    plain_text = plano.replace(' ', '')

print("Texto plano: ", plain_text)


# 2. Lista de genes de importancia clínica en salud mental
genes = ["ABCB1", "ADRA2A", "5HT2C", "HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1",
         "CYP3A4", "CYP3A5", "COMT", "DRD2", "GRIK1", "GRIK4", "HLA-A", "HLA-B", "HTR2A", "MC4R", "MTHFR", "NAT2",
         "OPRM1", "SLC6A4", "TPMT", "UGT1A1", "UGT1A4", "UGT2B15"]
print("Lista de genes en el archivo: ", genes)

# Genomind: variantes pegadas
# Oneome: variantes pegadas
# Novogenia:

# 3. Búsqueda de rs en archivos
patron = r"rs\d+"
busqueda = re.findall(patron, plain_text)
print("Lista de rs en el archivo: ", busqueda)
