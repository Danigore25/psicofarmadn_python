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
        handle = Entrez.esearch(db="gene", term=gen_full, sort="relevance")
        record5 = Entrez.read(handle)
        print("Busqueda en gene: ", record5['IdList'])
        handle = Entrez.esummary(db="gene", id=record5['IdList'][0])
        print("Gene data: ", Entrez.read(handle))
        handle.close()

    # DEFINIR FUNCIONES
    def ensembl_gen(gene_name):
        var_url_ensembl = "https://rest.ensembl.org"
        ext = "/x_refs/symbol/homo_sapiens/"
        response5 = requests.get(var_url_ensembl + ext + gene_name + "?", headers={"Content-Type": "application/json"})
        decoded = response5.json()
        print(repr(decoded))

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
        response5 = requests.get(var_url_ensembl + ext + reg + allele_1, headers={"Content-Type": "application/json"})
        decoded = response5.json()
        print("Busqueda en ensembl: ", repr(decoded))

    def pharm_geno(genotipo, gen_name):
        var_url5 = "https://api.pharmgkb.org/v1/data/haplotype/"
        response4 = requests.get(var_url5, [("name", genotipo), ("gene.symbol", gen_name)])
        print("Respuesta: ", response4.json())

    def pharm_alleles(allele, gen_name):
        var_url4 = "https://api.pharmgkb.org/v1/data/haplotype/"
        response4 = requests.get(var_url4, [("alleles.allele", allele), ("gene.symbol", gen_name)])
        print("Respuesta: ", response4.json())

    def pharmgkb_dip(gen_name, al1, al2):
        var_url3 = "https://api.pharmgkb.org/v1/data/diplotype/"
        response4 = requests.get(var_url3, [("gene.symbol", gen_name), ("allele1", al1), ("allele2", al2)])
        print("Respuesta: ", response4.json())

    def pubmed(genotipo):
        handle2 = Entrez.esearch(db="pubmed", term=genotipo)
        record4 = Entrez.read(handle2)
        print("IDs de la variante en pubmed: ", record4['IdList'])
        handle2 = Entrez.esummary(db="pubmed", id=record4['IdList'][0])
        print("Descripción del primer id (", record4['IdList'][0], ") de la variante en pubmed: ", Entrez.read(handle2))
        handle2.close()

    def pharmvar_al(variante):
        var_url7 = "https://www.pharmvar.org/api-service/alleles/"
        response6 = requests.get(var_url7, [("identifier", variante)])
        print("Respuesta: ", response6.json())


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
        todo = r'\D\/\D'
        gen = re.sub(todo, "", var)
        gene(gen)

        antes = r'\/\w+'
        despues = r'\D\/'
        g1 = re.sub(antes, "", var)
        g2 = re.sub(despues, "", var)
        if g1 == g2:
            alle = re.sub(gen, "", g1)
            pharm_alleles(alle, gen)
            ensembl_gen(gen)

        else:
            print(ensembl_gen(gen))
            all1 = re.sub(gen, "", g1)
            all2 = re.sub(gen, "", g2)
            pharm_alleles(all1, gen)
            pharm_alleles(all2, gen)
        print(var)

    elif geno2_search:
        todo = r'\*\w+'
        gen = re.sub(todo, "", var)
        gene(gen)
        res1 = r'^\w+'
        alelo1 = re.sub(res1, "", var)
        pharm_geno(alelo1, gen)

    elif geno3_search:
        todo = r'\*\w+\/\*\w+'
        gen = re.sub(todo, "", var)
        gene(gen)
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
        todo = r'\*\w+\/\*\w+'
        gen = re.sub(todo, "", var)
        gene(gen)

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
