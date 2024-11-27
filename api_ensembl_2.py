from Bio import Entrez
import requests
import re

Entrez.email = 'dgoretti@lcg.unam.mx'

# Notaciones ejemplos: ANK3C/C, CYP1A2*1B, CYP2B6*4/*5, CYP2C9*1F/*1F, genomind: ABCB1CYP1A2EM*1B

# FUNCIONES


def gene(gen_full):
    handle = Entrez.esearch(db="gene", term=gen_full, sort="relevance")
    record5 = Entrez.read(handle)
    handle = Entrez.esummary(db="gene", id=record5['IdList'][0])
    print("Gene data: ", Entrez.read(handle))
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
    response5 = requests.get(var_url_ensembl + ext + reg + "/" + allele_1, headers={"Content-Type": "application/json"})
    decoded = response5.json()
    print("Busqueda en ensembl: ", repr(decoded))


def rs_allele(rs_al):
    var_url_ensembl = "https://rest.ensembl.org"
    ext = "/variation/human/"
    response5 = requests.get(var_url_ensembl + ext + rs_al, headers={"Content-Type": "application/json"})
    decoded = response5.json()
    return decoded['mappings'][0]['location']


print("Escriba el nombre de la variante que desee buscar: ")
var = input()

# print("Escriba el ID del gen: ")  # ENSG00000151150
# gen_id = input()

print("Escriba el rs que desee buscar: ")  # rs10994336
rs = input()

# print("Escriba la posicion del rs: ")  # 10:60420054-60420054
# pos = input()

todo = r'\D\/\D'
gen = re.sub(todo, "", var)
antes = r'\/\w+'
despues = r'\D\/'
g1 = re.sub(antes, "", var)
g2 = re.sub(despues, "", var)
alle = re.sub(gen, "", g1)

gene(gen)
gen_id = ensembl_gen(gen)
ens_pheno(gen_id)
pos = rs_allele(rs)
ensembl(alle, pos)
