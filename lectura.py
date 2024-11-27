from Bio import Entrez
from pdfreader import SimplePDFViewer, PageDoesNotExist

# Pedir archivo PDF
print("Abrir el archivo.")
pdf_file = open('C:/Users/danig/OneDrive/Documentos/INMEGEN/Genomind_AdrianaVega.pdf', "rb")
viewer = SimplePDFViewer(pdf_file)
images = []
strings = []
try:
    while True:
        viewer.render()
        images.extend(viewer.canvas.inline_images)
        images.extend(viewer.canvas.images.values())
        strings.extend(viewer.canvas.strings)
        viewer.next()
except PageDoesNotExist:
    pass

text = "".join(strings)
print(text)

"5HT2C rs3813929; ABCB1 C3435T rs1045642; ABCB1 rs2032583; ADRA2A rs1800544; ANK3 rs10994336; BDNF rs6265; CACNA1C rs1006737; COMT rs4680; CYP1A2 *1B, *1C, *1D, *1E, *1F, *1K and *11; CYP2B6 *4, *5, and *6; CYP2C19 *2, *3, *4, *5, *6, *7, *8, *9, *10, *17, and *35; CYP2C9 *2, *3, *4, *5, *6, *8, *11, *13, and *27; CYP2D6 *2, *3, *4, gene deletion (*5), gene duplication, *6, *7, *8, *9, *10, *11, *12, *14, *15, *17, *29 and *41; CYP3A4 *22; CYP3A5 *3, *6, *7; DRD2 rs1799732; GRIK1 rs2832407; HLA-B*15:02 presence with reflex testing for presence of HLA-B*15:13 for all positive samples and Sanger sequencing for all double positive samples; HLA-A*31:01 rs1061235; HTR2A rs7997012; MC4R rs489693; MTHFR rs1801131 and rs1801133; OPRM1 rs1799971; SLC6A4 rs25531 and rs63749047; UGT2B15 rs1902023; and UGT1A4 rs2011425"


# C:/Users/danig/OneDrive/Documentos/INMEGEN/Genomind_AdrianaVega.pdf



# Buscar farmacogenes en bio.seqio
Entrez.email = 'dgoretti@lcg.unam.mx'

# Searching rs
handle = Entrez.esearch(db="clinvar", term="rs4680")
record = Entrez.read(handle)

handle = Entrez.esummary(db="clinvar", id=record["IdList"][0])
record2 = Entrez.read(handle)
# trait_xrefs
print(record2['DocumentSummarySet']['DocumentSummary'][0]['germline_classification'])
print(record2['DocumentSummarySet']['DocumentSummary'][0]['variation_set'])

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

