from Bio import Entrez

'''
# Pedir archivo PDF
print("Escriba la ruta del archivo: ")
archivo_input = input()
pdfread = textract.process(archivo_input, method='PDFminer')

# Pedir formato/tipo de archivo
print("Escriba el tipo de archivo: ")
formato_input = input()
'''

# Hacer lista de farmacogenes
genes_list = ['CYP1A2', 'CYP2B6', 'CYP2C9', 'CYP2C19', 'CYP2C', 'CYP2D6', 'CYP3A4', 'CYP3A5', 'CYP4F2', 'COMT', 'DPYD',
              'DRD2', 'F2', 'F5', 'GRIK4', 'HLA-A', 'HLA-B', 'HTR2A', 'HTR2C', 'IFNL4', 'NUDT15', 'OPRM1', 'SCL6A4',
              'SLCO1B1', 'TPMT', 'UGT1A1', 'BKORC1']

pharms = ['citalopram', 'escitalopram', 'fluoxetine', 'fluvoxamine', 'paroxetine', 'sertraline', 'desvenlafaxine',
          'duloxetine', 'levomilnacipran', 'venlafaxine', 'bupropion', 'esketamine', 'mirtazapine', 'nefazodone',
          'tradozone', 'vilazodone', 'vortioxetine', 'amitriptyline', 'amoxapine', 'clomipramine', 'desipramine',
          'doxepin', 'imipramine', 'nortriptyline', 'protriptyline', 'trimipramine', 'phenelzine', 'selegiline',
          'tranylcypromine', 'carbamazepine', 'gabapentin', 'lamotrigine', 'lithium', 'oxcarbazepine', 'pregabalin',
          'topiramate', 'valproate', 'aripiprazole', 'asenapine', 'brexpiprazole', 'cariprazine', 'clozapine',
          'iloperidone', 'lurasidone', 'olanzapine', 'paliperidone', 'pimavanserin', 'quetiapine', 'risperidone',
          'ziprasidone', 'chlorpromazine', 'fluphenazine', 'haloperidol', 'loxapine', 'perphenazine', 'pimozide',
          'thioridazine', 'thiothixene', 'trifluoperazine', 'alprazolam', 'buspirone', 'clonazepam', 'clorazepate',
          'chlordiazepoxide', 'diazepam', 'hydroxyzine', 'lorazepam', 'oxazepam', 'temazepam',
          'amphetamine-dextroamphetamine', 'dexmethylphenidate', 'dextroamphetamine', 'lisdexamfetamine',
          'methamphetamine', 'methylphenidate', 'atomoxetine', 'clonidine', 'guanfacine', 'L-methylfolate',
          'armodafinil', 'eszopiclone', 'modafinil', 'ramelteon', 'suvorexant', 'zaleplon', 'zolpidem', 'acetaminophen',
          'celecoxib', 'diclofenac', 'flurbiprofen', 'ibuprofen', 'ketorolac', 'meloxicam', 'naproxen', 'piroxicam',
          'alfentanil', 'codeine', 'fentanyl', 'hydrocodone', 'hydromorphone', 'meperidine', 'methadone', 'morphine',
          'oxycodone', 'oxymorphone', 'tapentadol', 'tramadol', 'dextromethorphan/quinidine', 'baclofen',
          'buprenorphine/naloxone', 'buprenorphine', 'cannibidiol', 'carisoprodol', 'cyclobenzaprine',
          'deutetrabenazine', 'metaxalone', 'methocarbamol', 'naltrexone', 'phenytoin/fosphenytoin', 'tizanidine',
          'valbenazine']

# Buscar farmacogenes en bio.seqio
Entrez.email = 'dgoretti@lcg.unam.mx'

# IMPRIMIR TODAS LAS BASES
handle = Entrez.einfo()
record100 = Entrez.read(handle)
print("Bases de datos Entrez: ", record100['DbList'])

handle = Entrez.esearch(db="gene", term="Homo sapiens[Org] AND COMT[Gene]")
record = Entrez.read(handle)
print("Gen: ", "COMT", ", id: ", record['IdList'][0])

# Name: 'ClinVar' in DbInfo, 'Related gene-specific medical variations' - clinvar, 'dbVar', 'MedGen'
handle = Entrez.esummary(db="gene", id=record['IdList'][0])
record1 = Entrez.read(handle)
print("Gene data: ", record1)

# Searching rs
# info2 = Entrez.einfo(db="clinvar")
# record_i = Entrez.read(info2)
# print("Info de clinvar: ", record_i)

handle = Entrez.esearch(db="clinvar", term="rs4680")
record2 = Entrez.read(handle)
print("clinvar lista: ", record2)
print("clinvar ID: ", record2["IdList"][0])

# GENE
handle = Entrez.esearch(db="gene", term="rs4680", sort="relevance")
recordsnp = Entrez.read(handle)
print("rs gene search: ", recordsnp)

handle = Entrez.esummary(db="gene", id=recordsnp['IdList'][0])
print("Busqueda de gen de snp: ", Entrez.read(handle))

# SNP
handle = Entrez.esearch(db="snp", term="rs4680")  # BUSCAR EN API
record4 = Entrez.read(handle)
print("rs ID search: ", record4)

handle = Entrez.esummary(db="snp", id=record4['IdList'][0])
record5 = Entrez.read(handle)
print("summary de snp: ", record5)

# OMIM
handle = Entrez.esearch(db="omim", term="rs4680")
recordom = Entrez.read(handle)
print("rs omim: ", recordom)

handle = Entrez.esummary(db="omim", id=recordom['IdList'][0:2])  # IMPRIMIR
record_omim = Entrez.read(handle)
print("record omim: ", record_omim)

'''
handle = Entrez.esearch(db="clinvar", term=record2['IdList'][0])
record6 = Entrez.read(handle)
print("busqueda en clinvar: ", record6)

handle = Entrez.esummary(db="clinvar", id=record6['IdList'][0])
record7 = Entrez.read(handle)
print("Busqueda de rs en clinvar: ", record7)

handle = Entrez.esearch(db="snp", term="CYP2C9*2[Name of the variant]", sort="relevance")
record3 = Entrez.read(handle)
print("var ID: ", record3)
print("variant number: ", record3["IdList"][0])

handle = Entrez.egquery(term="CYP2C9*2[Name of the variant]")
recordclin = Entrez.read(handle)
print("var ID: ", recordclin)
'''

# trait_xrefs
'''
print("Germline: ", record8['DocumentSummarySet']['DocumentSummary'][0]['germline_classification'])
# print("Variation: ", record8['DocumentSummarySet']['DocumentSummary'][0]['variation_set'])
print("Submissions: ", record8['DocumentSummarySet']['DocumentSummary'])
print("Databases: ", record8['DocumentSummarySet']['DocumentSummary'][0]['variation_set'][0]['variation_xrefs'])
print("omim: ", record8['DocumentSummarySet']['DocumentSummary'][0]['variation_set'][0]['variation_xrefs'][4])
print("rcv: ", record8['DocumentSummarySet']['DocumentSummary'][0]['supporting_submissions']['rcv'])
'''

info = Entrez.esummary(db="snp", id=record2["IdList"][0])
record5 = Entrez.read(info)
print("snp busqueda: ", record5)
info.close()
         
handle = Entrez.efetch(db="snp", id=record2["IdList"][0], rettype="docset", retmode="text")
print("snp fetch: ", handle.readline().strip())

handle = Entrez.esearch(db="pubmed", term="rs4680")
recordglo = Entrez.read(handle)
print("Busqueda pubmed", recordglo)
handle = Entrez.esummary(db="pubmed", id=recordglo['IdList'][0])
print("Summary de un articulo de pubmed: ", Entrez.read(handle))

# OTRAS BASES (GTR)

handle = Entrez.esearch(db="gtr", term="rs4680")
intento = Entrez.read(handle)
print("Intento de busqueda: ", intento)

handle = Entrez.esummary(db="gtr", id=intento['IdList'][0:4])
intento2 = Entrez.read(handle)
print("Resultados de intento: ", intento2)

handle = Entrez.efetch(db="clinvar", id=record2['IdList'][0], rettype="uilist", retmode="text")
clinvar_fetch = handle.readline().strip()
print("clinvar fetch: ", clinvar_fetch)

handle = Entrez.esearch(db="clinvar", term=clinvar_fetch)
record11 = Entrez.read(handle)
print("Intento clinvar: ", record11)


handle.close()

'''
i = -1
for gen in genes_list:
    handle = Entrez.esearch(db="gene", term=gen)
    record = Entrez.read(handle)
    print("Gen: ", gen, ", id: ", record['IdList'][0])
    handle = Entrez.efetch(db="gene", id = record['IdList'][0], retmode="xml")
    record1 = Entrez.read(handle, "genbank")
    # print(record1[0]['Entrezgene_gene']['Gene-ref']['Gene-ref_syn'])
    print(record1[0])
    handle.close()
'''
