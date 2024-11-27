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

if industry == "Genomind":
    start_page = 2
    final_page = 5
    for page in range(start_page, final_page):
        viewer.navigate(page)
else:
    start_page = 10
    final_page = 15
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

# 2. Lista de genes de importancia clínica en salud mental
genes = ["ABCB1", "ADRA2A", "5HT2C/HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1",
         "CYP3A4", "CYP3A5", "COMT", "DRD2", "GRIK1", "GRIK4", "HLA-A", "HLA-B", "HTR2A", "MC4R", "MTHFR", "NAT2",
         "OPRM1", "SCL6A4", "TPMT", "UGT1A1", "UGT1A4", "UGT2B15"]

# Genomind: variantes pegadas
# Oneome: variantes pegadas
# Novogenia:

# 3. Buscar genes y genotipos * en archivos

print("Lista de genes en el archivo: ", genes)
genotipos = []

for g in genes:
    patron = g + "\W\d+\W+\d+"
    busqueda1 = re.findall(patron, plain_text)
    if len(busqueda1) != 0:
        print("Opciones del gen", g, ": ", busqueda1)
        genotipos.extend(busqueda1)
    patron2 = g + "\w+\W\w+"
    busqueda2 = re.findall(patron2, plain_text)
    if len(busqueda2) != 0:
        print("Otras opciones: ", busqueda2)
        genotipos.extend(busqueda2)

print("Genotipos en total: ", genotipos)
print(len(genotipos))

# Eliminar genotipos repetidos
genotipos_unicos = []
for genotipo in genotipos:
    if genotipo not in genotipos_unicos:
        genotipos_unicos.append(genotipo)

print("Genotipos unicos: ", genotipos_unicos)
print(len(genotipos_unicos))

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

        handle = Entrez.esummary(db="snp", id=record["IdList"][0])
        record2 = Entrez.read(handle)
        print("Datos completos del rs: ", record2)
        print("Frecuencia del rs: ", record2['DocumentSummarySet']['DocumentSummary'][0]['GLOBAL_MAFS'])

        handle = Entrez.esearch(db="gene", term=rs)
        record1 = Entrez.read(handle)
        handle = Entrez.esummary(db="gene", id=record1["IdList"][0])
        recordgene = Entrez.read(handle)
        print("Gen del rs: ", recordgene['DocumentSummarySet']['DocumentSummary'])

        # USAR OMIM EN VEZ DE CLINVAR, HACER SNP FETCH, HACER API DE CLINVAR
        '''handle = Entrez.esearch(db="clinvar", term=rs)
        record2 = Entrez.read(handle)
        print("Clinvar ids: ", record2['IdList'])
        for clin in record2['IdList']:
            handle = Entrez.esummary(db="clinvar", id=clin)
            print("Summary de clinvar id ", clin, ": ", Entrez.read(handle))
            '''
        '''
        clinvar_url = "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/"
        response2 = requests.get(clinvar_url, [("id", pharm_id), ("view", "max")])
        print("Prueba clinvar: ", response2.json())

        var_url2 = "https://api.pharmgkb.org/v1/data/clinicalAnnotation/"
        response3 = requests.get(var_url2, [("id", pharm_id), ("view", "max")])
        print("Fenotipos: ", response3.json())
        '''
        handle = Entrez.esearch(db="omim", term=rs)
        response4 = Entrez.read(handle)
        print("IDs del rs en OMIM: ", response4['IdList'])
        for omi in response4['IdList']:
            handle = Entrez.esummary(db="omim", id=omi)
            print("Descripción del rs con el id ", omi, "en OMIM: ", Entrez.read(handle))

        handle = Entrez.esearch(db="pubmed", term=rs)
        record4 = Entrez.read(handle)
        print("IDs del rs en pubmed: ", record4['IdList'])
        handle = Entrez.esummary(db="pubmed", id=record4['IdList'][0])
        print("Descripción del primer id (", record4['IdList'][0], ") del rs en pubmed: ", Entrez.read(handle))
        '''
        for id in record4['IdList']:
            handle = Entrez.esummary(db="pubmed", id=id)
            print("Summary de pubmed id ", id, ": ", Entrez.read(handle))
        '''
    except IndexError:
        pass

# AHORA HAREMOS LO MISMO CON LOS ALELOS DE FORMA *
# FUTURO: VER SI SE PUEDE HACER UNA FUNCION PARA AMBOS TIPOS DE NOTACION
print("VARIANTES DE FORMA NAME*NUMBER")
for var in genotipos_unicos:
    try:
        print("Nombre de la variante: ", var)
        handle = Entrez.esearch(db="snp", term=var)
        record = Entrez.read(handle)

        handle = Entrez.esummary(db="snp", id=record["IdList"][0])
        record2 = Entrez.read(handle)
        print("Datos completos de la variante: ", record2)
        print("Frecuencia de la variante: ", record2['DocumentSummarySet']['DocumentSummary'][0]['GLOBAL_MAFS'])

        handle = Entrez.esearch(db="gene", term=var)
        record1 = Entrez.read(handle)
        handle = Entrez.esummary(db="gene", id=record1["IdList"][0])
        recordgene = Entrez.read(handle)
        print("Gen de la variante: ", recordgene['DocumentSummarySet']['DocumentSummary'])

        handle = Entrez.esearch(db="omim", term=var)
        response4 = Entrez.read(handle)
        print("IDs de la variante en OMIM: ", response4['IdList'])
        for omi in response4['IdList']:
            handle = Entrez.esummary(db="omim", id=omi)
            print("Descripción de la variante con el id ", omi, "en OMIM: ", Entrez.read(handle))

        handle = Entrez.esearch(db="pubmed", term=var)
        record4 = Entrez.read(handle)
        print("IDs de la variante en pubmed: ", record4['IdList'])
        handle = Entrez.esummary(db="pubmed", id=record4['IdList'][0])
        print("Descripción del primer id (", record4['IdList'][0], ") de la variante en pubmed: ", Entrez.read(handle))
        '''
        for id in record4['IdList']:
            handle = Entrez.esummary(db="pubmed", id=id)
            print("Summary de pubmed id ", id, ": ", Entrez.read(handle))
        '''
    except IndexError:
        pass
