# Prueba de busqueda de rs en archivo  bim convertido a texto
# 1. Importar librerias
from Bio import Entrez
import re

Entrez.email = 'dgoretti@lcg.unam.mx'

# 2. Abrir archivo
bimfile = open('C:/Users/danig/grad_thesis/mxgdar_controles.txt')
texto = bimfile.read()

# 3. Buscar cadena de texto
patron = "rs\d+"
busqueda = re.findall(patron, texto)
print(busqueda)

# Searching rs
for rs in busqueda:
    handle = Entrez.esearch(db="snp", term=rs)
    record = Entrez.read(handle)

    handle = Entrez.efetch(db="snp", id=record["IdList"][0], rettype="docset", retmode="text")
    print(handle.readline().strip())
    handle.close()
