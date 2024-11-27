# ESTO ES DISTINTO AL ARCHIVO DE genotipos.py, ES SOLO UNA PRUEBA PARA REVISAR COMO BUSCAR LOS GENOTIPOS
# INDEPENDIENTEMENTE DE LA NOTACION

from Bio import Entrez
import re
import requests

Entrez.email = 'dgoretti@lcg.unam.mx'

# Notaciones ejemplos: ANK3C/C, CYP1A2*1B, CYP2B6*4/*5, CYP2C9*1F/*1F, genomind: ABCB1CYP1A2EM*1B

# En genomind:
ejemplos = ['ANK3C/C', 'CYP1A2*1B', 'CYP2B6*4/*5', 'CYP2C9*1F/*1F', 'ABCB1CYP1A2EM*1B']
print("Estos son los genotipos de ejemplo: ", ejemplos)

genotipos_cor = []

for geno in ejemplos:
    patron4 = r'\DM'
    correc = re.sub(patron4, "", geno)
    genotipos_cor.append(correc)

print("Genotipos de ejemplo corregidos: ", genotipos_cor)

print("Introduzca la variante que desee buscar: ")
var = input()

if var in genotipos_cor:
    # BUSQUEDA EN NCBI (NUCLEOTIDE; CLINVAR, OMIM)
    def gene(gen_full):
        handle = Entrez.esearch(db="gene", term=gen_full)
        record5 = Entrez.read(handle)
        print("Busqueda en gene: ", record5['IdList'])
        handle = Entrez.esummary(db="gene", id=record5['IdList'][0])
        print("Gene data: ", Entrez.read(handle))
        handle.close()

    # DEFINIR FUNCIONES
    def ensembl(genotipo):
        var_url_ensembl = "https://rest.ensembl.org"
        ext = "/variant_recoder/human/"
        response5 = requests.get(var_url_ensembl + ext + genotipo, headers={"Content-Type": "application/json"})
        decoded = response5.json()
        print("Busqueda en ensembl: ", repr(decoded))

    def pharmgkb(genotipo):
        var_url3 = "https://api.pharmgkb.org/v1/data/variant/"
        response4 = requests.get(var_url3, [("name", genotipo)])
        print("Respuesta: ", response4.json())

    def pubmed(genotipo):
        handle2 = Entrez.esearch(db="pubmed", term=genotipo)
        record4 = Entrez.read(handle2)
        print("IDs de la variante en pubmed: ", record4['IdList'])
        handle2 = Entrez.esummary(db="pubmed", id=record4['IdList'][0])
        print("Descripción del primer id (", record4['IdList'][0], ") de la variante en pubmed: ", Entrez.read(handle2))
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
