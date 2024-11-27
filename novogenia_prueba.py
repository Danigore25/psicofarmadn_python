from pdfreader import SimplePDFViewer
from PyPDF2 import PdfReader

print("Escriba la industria a la que pertenecen sus resultados (Oneome, Genomind, Novogenia)")
industry = input()
print("Escriba la ruta del archivo PDF: ")

# b) 'C:/Users/danig/Downloads/M8I9347-REPORT-SofiaJastrow.pdf'
# c) 'C:/Users/danig/Downloads/oneome-report-A4E01.pdf'

pdf_file = open(input(), "rb")
viewer = SimplePDFViewer(pdf_file)

strings = []
'''
if industry == "Genomind":
    start_page = 2
    final_page = 5
    for page in range(start_page, final_page):
        viewer.navigate(page)
if industry == "Oneome":
    start_page = 11
    final_page = 14
    for page in range(start_page, final_page):
        viewer.navigate(page)
else:
    plain_text = ""
    start_page = 14
    final_page = 16
    for page in range(start_page, final_page):
        viewer.navigate(page)


plain_text = ""

try:
    while True:
        viewer.render()
        plain_text += "".join(viewer.canvas.strings)
        viewer.next()
except PageDoesNotExist:
    pass

print(plain_text)
'''

# INTENTO DE LECTURA DE ARCHIVO NOVOGENIA - NO SALIO
'''
images = []
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
print(text)
'''

# INTENTO 2
PDF_read = PdfReader(pdf_file)
for page in range(13, 16):
    first_page = PDF_read.pages[page]  # 13 a 15
    print(first_page.extract_text())
