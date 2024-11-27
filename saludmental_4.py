# PROGRAMA PARA DETECTAR VARIANTES FARMACOGENÓMICAS RELACIONADAS CON MEDICAMENTOS PSIQUIATRICOS
# 1. Abrir librerias
from Bio import Entrez
from pdfreader import SimplePDFViewer, PageDoesNotExist
from PyPDF2 import PdfReader
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

if industry == "Genomind":
    start_page = 2
    final_page = 5
    for page in range(start_page, final_page):
        viewer.navigate(page)
    try:
        while True:
            viewer.render()
            plain_text += "".join(viewer.canvas.strings)
            viewer.next()
    except PageDoesNotExist:
        pass
elif industry == "Oneome":
    start_page = 10
    final_page = 13
    for page in range(start_page, final_page):
        viewer.navigate(page)
    try:
        while True:
            viewer.render()
            plain_text += "".join(viewer.canvas.strings)
            viewer.next()
    except PageDoesNotExist:
        pass
elif industry == "Novogenia":
    plain_full = ""
    PDF_read = PdfReader(pdf_file)
    for page in range(13, 16):
        pages = PDF_read.pages[page]  # 13 a 15
        plain_full += ''.join(pages.extract_text())
    plano = " ".join(plain_full.split())
    plain_text = plano.replace(' ', '')


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
print("VARIANTES DE FORMA NAME*NUMBER")
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
        patron = g + r"\W\d+\W+\d+"
        busqueda1 = re.findall(patron, plain_text)
        if len(busqueda1) != 0:
            genotipos.extend(busqueda1)
        patron2 = g + r"\w+\W\w+"
        busqueda2 = re.findall(patron2, plain_text)
        if len(busqueda2) != 0:
            genotipos.extend(busqueda2)

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


print("Escriba la variante genotipica que desee buscar: ")
var = input()

if var in genotipos_unicos:
    try:
        print("Nombre de la variante: ", var)
        # DEFINIR FUNCIONES

        def gene(gen_full):
            handle2 = Entrez.esearch(db="gene", term=gen_full)
            record5 = Entrez.read(handle2)
            print("Busqueda en gene: ", record5['IdList'])
            handle2 = Entrez.esummary(db="gene", id=record5['IdList'][0])
            print("Gene data: ", Entrez.read(handle2))
            handle.close()

        def ensembl(geno_ens):
            var_url_ensembl = "https://rest.ensembl.org"
            ext = "/variant_recoder/human/"
            response5 = requests.get(var_url_ensembl + ext + geno_ens, headers={"Content-Type": "application/json"})
            decoded = response5.json()
            print("Busqueda en ensembl: ", repr(decoded))

        def pharmgkb(geno_pharm):
            var_url3 = "https://api.pharmgkb.org/v1/data/variant/"
            response5 = requests.get(var_url3, [("name", geno_pharm)])
            print("Respuesta: ", response5.json())

        def pubmed(geno_pub):
            handle2 = Entrez.esearch(db="pubmed", term=geno_pub)
            record5 = Entrez.read(handle2)
            print("IDs de la variante en pubmed: ", record5['IdList'])
            handle2 = Entrez.esummary(db="pubmed", id=record5['IdList'][0])
            print("Descripción del primer id (", record5['IdList'][0], ") de la variante en pubmed: ",
                  Entrez.read(handle2))
            handle2.close()

        # SEPARAR SEGUN GENOTIPO:
        geno1 = r"\w+\/\w{1,3}"
        geno2 = r'\w+\*\w{1,2}$'
        geno3 = r'\w+\*\d\/\*\d'
        geno4 = r'\w+\*\d+\D\/\*\d+\D'

        geno1_search = re.findall(geno1, var)
        geno2_search = re.findall(geno2, var)
        geno3_search = re.findall(geno3, var)
        geno4_search = re.findall(geno4, var)

        if geno1_search:
            todo = r'\D\/\D'
            gen = re.sub(todo, "", var)
            gene(gen)

            antes = r'\/\w+'
            despues = r'\D\/'
            g1 = re.sub(antes, "", var)
            g2 = re.sub(despues, "", var)
            if g1 == g2:
                ensembl(g1)
            else:
                ensembl(g1)
                ensembl(g2)

        elif geno2_search:
            todo = r'\*\w+'
            gen = re.sub(todo, "", var)
            gene(gen)
            pharmgkb(var)

        elif geno3_search:
            todo = r'\*\w+'
            gen = re.sub(todo, "", var)
            gene(gen)
            pubmed(var)
            antes = r'\/\*\w+'
            despues = r'\*\w+\/'
            g1 = re.sub(antes, "", var)
            g2 = re.sub(despues, "", var)
            if g1 == g2:
                pharmgkb(g1)
            else:
                pharmgkb(g1)
                pharmgkb(g2)

        elif geno4_search:
            todo = r'\*\w+'
            gen = re.sub(todo, "", var)
            gene(gen)
            antes = r'\/\*\w+'
            despues = r'\*\w+\/'
            g1 = re.sub(antes, "", var)
            g2 = re.sub(despues, "", var)
            if g1 == g2:
                pubmed(g1)
            else:
                pubmed(g1)
                pubmed(g2)
    except IndexError:
        pass
