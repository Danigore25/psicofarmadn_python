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

# 2. Lista de genes de importancia clínica en salud mental
genes = ["ABCB1", "ADRA2A", "5HT2C/HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1",
         "CYP3A4", "CYP3A5", "COMT", "DRD2", "GRIK1", "GRIK4", "HLA-A", "HLA-B", "HTR2A", "MC4R", "MTHFR", "NAT2",
         "OPRM1", "SCL6A4", "TPMT", "UGT1A1", "UGT1A4", "UGT2B15"]
print("Lista de genes en el archivo: ", genes)

# Genomind: variantes pegadas
# Oneome: variantes pegadas
# Novogenia:

# 3. Búsqueda de rs en archivos
patron = r"rs\d+"
busqueda = re.findall(patron, plain_text)
print("Lista de rs en el archivo: ", busqueda)

# 4. Buscar rs y genotipos * en archivos
# Imprimir nombre de rs, los datos de snp del rs, la frecuencia en snp, el gen de donde proviene, buscar pharm_id y
# los fenotipos

Entrez.email = 'dgoretti@lcg.unam.mx'

print("Escriba el rs que desee buscar: ")
rs = input()

if rs in busqueda:
    try:
        print("Nombre de rs: ", rs)
        handle = Entrez.esearch(db="snp", term=rs)
        record = Entrez.read(handle)

        handle = Entrez.esummary(db="snp", id=record["IdList"][0])
        record2 = Entrez.read(handle)
        print("Datos completos del rs: ", record2)
        print("ID del snp: : ", record2['DocumentSummarySet']['DocumentSummary'][0]['SNP_ID'])
        print("Significancia clinica general del rs: ", record2['DocumentSummarySet']['DocumentSummary'][0]
        ['CLINICAL_SIGNIFICANCE'])
        print("Tipo de snp: ", record2['DocumentSummarySet']['DocumentSummary'][0]['SNP_CLASS'])
        print("Posicion: ", record2['DocumentSummarySet']['DocumentSummary'][0]['CHRPOS'])
        print("Frecuencia del rs: ", record2['DocumentSummarySet']['DocumentSummary'][0]['GLOBAL_MAFS'])

        handle = Entrez.esearch(db="gene", term=rs, sort="relevance")
        record1 = Entrez.read(handle)
        handle = Entrez.esummary(db="gene", id=record1["IdList"][0])
        recordgene = Entrez.read(handle)
        print("Gen del rs: ", recordgene['DocumentSummarySet']['DocumentSummary'][0])

        # USAR OMIM EN VEZ DE CLINVAR, HACER SNP FETCH, HACER API DE CLINVAR

        var_url = "https://api.pharmgkb.org/v1/data/variant/"
        response3 = requests.get(var_url, [("symbol", rs), ("view", "base")])
        print("Datos pharmgkb: ", response3.json())
        pharm_gkb = response3.json()
        pharm_id = pharm_gkb['data'][0]['id']
        print("ID en pharmgkb: ", pharm_id)

        var_url2 = "https://api.pharmgkb.org/v1/data/clinicalAnnotation/"
        response3 = requests.get(var_url2, [("location.fingerprint", rs), ("view", "min")])
        print("Fenotipos: ", response3.json())

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

        handle.close()
    except IndexError:
        pass

# AHORA HAREMOS LO MISMO CON LOS ALELOS DE FORMA *
# FUTURO: VER SI SE PUEDE HACER UNA FUNCION PARA AMBOS TIPOS DE NOTACION

# 5. Buscar genes y genotipos * en archivos
genotipos = []

for g in genes:
    patron = g + r"\W\d+\W+\d+"
    busqueda1 = re.findall(patron, plain_text)
    if len(busqueda1) != 0:
        genotipos.extend(busqueda1)
    patron2 = g + r"\w+\W\w+"
    busqueda2 = re.findall(patron2, plain_text)
    if len(busqueda2) != 0:
        genotipos.extend(busqueda2)


# Eliminar genotipos repetidos
genotipos_unicos = []
for genotipo in genotipos:
    if genotipo not in genotipos_unicos:
        genotipos_unicos.append(genotipo)

print("Genotipos unicos (", len(genotipos_unicos), "): ", genotipos_unicos)

print("VARIANTES DE FORMA NAME*NUMBER")
print("Escriba la variante genotipica que desee buscar: ")
var = input()

if var in genotipos_unicos:
    try:
        print("Nombre de la variante: ", var)

        # BUSQUEDA EN NCBI (NUCLEOTIDE; CLINVAR, OMIM)
        handle = Entrez.esearch(db="nucleotide", term=var)
        record5 = Entrez.read(handle)
        print("Busqueda en nucleotide: ", record5['IdList'])
        handle = Entrez.esummary(db="nucleotide", id=record5['IdList'][0])
        print("Nucleotide data: ", Entrez.read(handle))

        handle = Entrez.esearch(db="clinvar", term=var)
        record6 = Entrez.read(handle)
        print("Busqueda en clinvar: ", record6['IdList'])
        handle = Entrez.esummary(db="clinvar", id=record6['IdList'][0])
        print("clinvar data: ", Entrez.read(handle))

        handle = Entrez.esearch(db="omim", term=var)
        record7 = Entrez.read(handle)
        print("Busqueda en omim: ", record7['IdList'])
        handle = Entrez.esummary(db="omim", id=record7['IdList'][0])
        print("omim data: ", Entrez.read(handle))

        # BUSQUEDA EN PHARMGKB
        var_url3 = "https://api.pharmgkb.org/v1/data/variant/"
        response4 = requests.get(var_url3, [("name", var)])
        print("Respuesta: ", response4.json())

        # BUSQUEDA EN ENSEMBL
        var_url_ensembl = "https://rest.ensembl.org"
        ext = "/variant_recoder/human/"
        response5 = requests.get(var_url_ensembl+ext+var, headers={"Content-Type": "application/json"})
        decoded = response5.json()
        print("Busqueda en ensembl: ", repr(decoded))

        # BUSQUEDA EN PUBMED
        handle = Entrez.esearch(db="pubmed", term=var)
        record4 = Entrez.read(handle)
        print("IDs de la variante en pubmed: ", record4['IdList'])
        handle = Entrez.esummary(db="pubmed", id=record4['IdList'][0])
        print("Descripción del primer id (", record4['IdList'][0], ") de la variante en pubmed: ", Entrez.read(handle))

        handle.close()
    except IndexError:
        pass
