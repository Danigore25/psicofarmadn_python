import re

print("Escriba el genotipo que desee analizar: ")
geno = input()


geno1 = r"\w+\/\w{1,3}"
geno2 = r'\w+\*\w{1,2}$'
geno3 = r'\w+\*\d\/\*\d'
geno4 = r'\w+\*\d+\D\/\*\d+\D'

geno1_search = re.findall(geno1, geno)
geno2_search = re.findall(geno2, geno)
geno3_search = re.findall(geno3, geno)
geno4_search = re.findall(geno4, geno)

if geno1_search:
    print("Geno1: ", geno)
elif geno2_search:
    print("Geno2: ", geno)
elif geno3_search:
    print("Geno3: ", geno)
elif geno4_search:
    print("Geno4: ", geno)
