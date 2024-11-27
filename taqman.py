# Abrir TaqMan Genotyper Software, extraer archivo AIF de ejemplo
# 1. Importar librerias
from Bio import Entrez
import re

Entrez.email = 'dgoretti@lcg.unam.mx'

# 2. Abrir archivo
taqman = open('C:/Users/danig/grad_thesis/AIF_Sample.txt')
texto = taqman.read()

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
