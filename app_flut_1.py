# PRUEBA DE APP FLUTTERFLOW
# PARTE FINAL 2 DEL PROGRAMA DE PYTHON APP: PETICION INPUT/OS DE VARIABLES
# 1. Abrir librerias
from Bio import Entrez
import re
import requests

# 2. Lista de genes de importancia clínica en salud mental
genes = ["ABCB1", "ADRA2A", "5HT2C", "HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1",
         "CYP3A4", "CYP3A5", "COMT", "DRD2", "GRIK1", "GRIK4", "HLA-A", "HLA-B", "HTR2A", "MC4R", "MTHFR", "NAT2",
         "OPRM1", "SLC6A4", "TPMT", "UGT1A1", "UGT1A4", "UGT2B15"]
print("Lista de genes propuestos de importancia psiquiátrica: ", genes)

# 3. Pedir rs
# Imprimir nombre de rs, los datos de snp del rs, la frecuencia en snp, el gen de donde proviene, buscar pharm_id y
# los fenotipos

Entrez.email = 'dgoretti@lcg.unam.mx'

print("Escriba el rs que desee buscar: ")
rs = input()

print("Escriba el nombre del farmaco que consume el paciente: ")
med = input()

try:
    handle = Entrez.esearch(db="snp", term=rs)
    record = Entrez.read(handle)

    handle = Entrez.esummary(db="snp", id=record["IdList"][0])
    record2 = Entrez.read(handle)
    print("Nombre de la variante: ", rs)
    print("Clinica general del rs: ", record2['DocumentSummarySet']['DocumentSummary'][0]['CLINICAL_SIGNIFICANCE'])
    print("Posicion: ", record2['DocumentSummarySet']['DocumentSummary'][0]['CHRPOS'])

    handle = Entrez.esearch(db="gene", term=rs, sort="relevance")
    record1 = Entrez.read(handle)
    handle = Entrez.esummary(db="gene", id=record1["IdList"][0])
    recordgene = Entrez.read(handle)
    print("Gen del rs: ", recordgene['DocumentSummarySet']['DocumentSummary'][0]['Name'])

    var_url = "https://api.pharmgkb.org/v1/data/clinicalAnnotation/"
    response3 = requests.get(var_url, [("location.fingerprint", rs), ("view", "min"),
                                       ("relatedChemicals.name", med)])
    print("Fenotipos: ", response3.json())

    var_url_ensembl1 = "https://rest.ensembl.org"
    exten = "/variation/human/"
    response_ens = requests.get(var_url_ensembl1 + exten + rs + "?pops=1", headers={"Content-Type": "application/json"})
    decoded0 = response_ens.json()
    # print("Frecuencia general: ", decoded0['populations'])
    list1 = decoded0['populations']
    for population in list1:
        if population['population'] == '1000GENOMES:phase_3:AMR':
            print("Incidencia latina: ", population)

    handle = Entrez.esearch(db="pubmed", term=rs)
    record4 = Entrez.read(handle)
    print("IDs del rs en pubmed: ", record4['IdList'])

    handle.close()
except IndexError:
    pass

# AHORA HAREMOS LO MISMO CON LOS ALELOS DE FORMA *

# 5. Buscar genes y genotipos * en archivos
print("VARIANTES DE FORMA NAME*NUMBER")

print("Escriba el gen que desee buscar: ")
gen = input()

print("Escriba el genotipo del gen que desea buscar:")
genotipo = input()

var = gen + genotipo

handle = Entrez.esearch(db="gene", term=gen, sort="relevance")
record5 = Entrez.read(handle)
handle = Entrez.esummary(db="gene", id=record5['IdList'][0])
record6 = Entrez.read(handle)
print("Gene name: ", record6['DocumentSummarySet']['DocumentSummary'][0]['Name'])
handle.close()

# DEFINIR FUNCIONES


def ensembl_gen(gene_name):
    var_url_ensembl = "https://rest.ensembl.org"
    ext = "/lookup/symbol/homo_sapiens/"
    response5 = requests.get(var_url_ensembl + ext + gene_name, headers={"Content-Type": "application/json"})
    decoded = response5.json()
    return decoded['id']


def ens_pheno(gene_id):
    var_url_ensembl = "https://rest.ensembl.org"
    ext = "/phenotype/gene/homo_sapiens/"
    response5 = requests.get(var_url_ensembl + ext + gene_id, headers={"Content-Type": "application/json"})
    decoded = response5.json()
    print("Fenotipo de gen en ensembl: ", repr(decoded))
    repr(decoded)


def ensembl(allele_1, reg):
    var_url_ensembl = "https://rest.ensembl.org"
    ext = "/vep/human/region/"
    response5 = requests.get(var_url_ensembl + ext + reg + "/" + allele_1,
                             headers={"Content-Type": "application/json"})
    decoded = response5.json()
    print("Busqueda de rs en ensembl: ", repr(decoded))


def rs_allele(rs_al):
    var_url_ensembl = "https://rest.ensembl.org"
    ext = "/variation/human/"
    response5 = requests.get(var_url_ensembl + ext + rs_al, headers={"Content-Type": "application/json"})
    decoded = response5.json()
    print("Datos del rs: ", repr(decoded['mappings']))
    return decoded['mappings'][0]['location']


def pharm_geno(genotype, gen_name):
    var_url5 = "https://api.pharmgkb.org/v1/data/haplotype/"
    response5 = requests.get(var_url5, [("name", genotype), ("gene.symbol", gen_name)])
    decoded = response5.json()
    print("Simbolo de haplotipo: ", decoded['data'][0]['symbol'])
    genotype_full = decoded['data'][0]['symbol']
    print("Actividad: ", decoded['data'][0]['activityValue'])
    haplo_id = decoded['data'][0]['id']
    print("Id de haplotipo en pharmgkb: ", haplo_id)
    print("Funcion: ", decoded['data'][0]['functionTerm']['term'])
    print("Posicion hgvs: ", decoded['data'][0]['hgvs'])

    # Checar clinical annotation
    var_url7 = "https://api.pharmgkb.org/v1/data/clinicalAnnotation/"
    response7 = requests.get(var_url7, [("location.haplotypes.accessionId", haplo_id), ("view", "min"),
                                        ("relatedChemicals.name", med)])
    decoded3 = response7.json()
    print("Anotacion clinica: ", decoded3)

    # Population - esearch and elink clinvar-snp
    handle3 = Entrez.esearch(db="clinvar", term=genotype_full)
    record8 = Entrez.read(handle3)
    clinvar_id = record8['IdList'][0]

    handle3 = Entrez.elink(dbfrom="clinvar", db="snp", id=clinvar_id)
    record9 = Entrez.read(handle3)
    print("Busqueda de variante clinvar-snp: ", record9[0]['LinkSetDb'][0]['Link'][0]['Id'])
    snp_id = record9[0]['LinkSetDb'][0]['Link'][0]['Id']

    handle3 = Entrez.esummary(db="snp", id=snp_id)
    record10 = Entrez.read(handle3)
    print("Summary de snp de haplotipo: ", record10)
    rs_snp = "rs" + snp_id
    print("rs asociado al haplotipo: ", rs_snp)

    var_url_ensembl2 = "https://rest.ensembl.org"
    extens = "/variation/human/"
    responsen = requests.get(var_url_ensembl2 + extens + rs_snp + "?pops=1",
                             headers={"Content-Type": "application/json"})
    decoded11 = responsen.json()

    print("Incidencia mundial: ", decoded11['populations'])
    lista = decoded11['populations']
    for popul in lista:
        if popul['population'] == '1000GENOMES:phase_3:AMR':
            print("Incidencia latina: ", popul)
    handle3.close()


def pubmed(genotype):
    handle2 = Entrez.esearch(db="pubmed", term=genotype)
    record7 = Entrez.read(handle2)
    print("IDs de la variante en pubmed: ", record7['IdList'])
    handle2.close()


def pharmvar_al(variante):
    var_url7 = "https://www.pharmvar.org/api-service/alleles/"
    response6 = requests.get(var_url7, [("identifier", variante)])
    print("Datos genotípicos: ", response6.json())


def popul(rs_id):
    handle1 = Entrez.esearch(db="snp", term=rs_id)
    record7 = Entrez.read(handle1)
    handle1 = Entrez.esummary(db="snp", id=record7["IdList"][0])
    record8 = Entrez.read(handle1)
    print("Frecuencia del snp: : ", record8['DocumentSummarySet']['DocumentSummary'][0]['GLOBAL_MAFS'])
    handle1.close()


def clinic(rs_id):
    var_url5 = "https://api.pharmgkb.org/v1/data/clinicalAnnotation/"
    response5 = requests.get(var_url5, [("location.fingerprint", rs_id), ("view", "min")])
    decoded = response5.json()
    print("Datos clinicos de la variante: ", decoded['data'])


# SEPARAR SEGUN GENOTIPO:
geno1 = r"\w+\/\w{1,3}"
geno2 = r'\w+\*\w{1,2}$'
geno3 = r'\w+\*\d\/\*\d'
geno4 = r'\w+\*\d{1,2}\w\/\*\d{1,2}\w'

geno1_search = re.findall(geno1, var)
geno2_search = re.findall(geno2, var)
geno3_search = re.findall(geno3, var)
geno4_search = re.findall(geno4, var)

if geno1_search:
    print("Escriba el rs que desee buscar: ")
    rs = input()
    antes = r'\/\w+'
    despues = r'\D\/'
    g1 = re.sub(antes, "", var)
    g2 = re.sub(despues, "", var)
    if g1 == g2:
        alle = re.sub(gen, "", g1)
        gen_id = ensembl_gen(gen)
        ens_pheno(gen_id)
        pos = rs_allele(rs)
        ensembl(alle, pos)
        popul(rs)
        clinic(rs)
    else:
        all1 = re.sub(gen, "", g1)
        all2 = re.sub(gen, "", g2)
        gen_id = ensembl_gen(gen)
        ens_pheno(gen_id)
        pos = rs_allele(rs)
        ensembl(all1, pos)
        ensembl(all2, pos)
        popul(rs)
        clinic(rs)

elif geno2_search:
    res1 = r'^\w+'
    alelo1 = re.sub(res1, "", var)
    pharm_geno(alelo1, gen)
    pubmed(var)

elif geno3_search:
    antes = r'\/\*\w+'
    despues = r'\*\w+\/'
    g1 = re.sub(antes, "", var)
    g2 = re.sub(despues, "", var)
    alelos = r'^\w+'
    if g1 == g2:
        alelo = re.sub(alelos, "", g1)
        pharm_geno(alelo, gen)
        pubmed(var)
    else:
        alelo1 = re.sub(alelos, "", g1)
        alelo2 = re.sub(alelos, "", g2)
        pharm_geno(alelo1, gen)
        pharm_geno(alelo2, gen)
        pubmed(var)

elif geno4_search:
    antes = r'\/\*\w+'
    despues = r'\*\w+\/'
    g1 = re.sub(antes, "", var)
    g2 = re.sub(despues, "", var)
    if g1 == g2:
        alle = re.sub(gen, "", g1)
        genot = gen + " " + alle
        alle_full = gen + alle
        pharmvar_al(alle_full)
        pubmed(genot)
    else:
        all1 = re.sub(gen, "", g1)
        all2 = re.sub(gen, "", g2)
        print(all1)
        genot1 = gen + " " + all1
        genot2 = gen + " " + all2
        ale1 = gen + all1
        ale2 = gen + all2
        pubmed(genot1)
        pubmed(genot2)
        pharmvar_al(ale1)
        pharmvar_al(ale2)
