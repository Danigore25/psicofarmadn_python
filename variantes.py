# Lista de farmacogenes y variantes

novagenic = ["CYP1A2", "CYP2B6", "CYP2C9", "CYP2C19", "CYP2C", "CYP2D6", "CYP3A4", "CYP3A5", "CYP4F2", "COMT", "DPYD",
             "DRD2", "F2", "F5", "GRIK4", "HLA_A", "HLA_B", "HTR2A", "HTR2C", "IFNL4", "NUDT15", "OPRM1", "SCL6A4",
             "SLCO1B1", "TPMT", "UGT1A1", "vKORC1"]

genomind = ["5HT2C", "ADRA2A", "ANK3", "FNDC", "CACNA1C", "COMT", "DRD2", "GRIK1", "HLA-A", "HLA-B", "HTR2A", "MC4R",
            "MTHFR", "OPRM1", "SCL6A4", "ABCB1", "UGT1A4", "UGT2B15", "CYP1A2", "CYP2B6", "CYP2C9", "CYP2C19", "CYP2D6",
            "CYP3A4/5"]

novogenia = ["CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1", "CYP3A4", "CYP3A5", "DPYD", "HLA-B*5701",
             "NAT2", "TPMT", "SLCO1B1", "VKORC1", "UGT1A1"]

genes = ["ABCB1", "ADRA2A", "5HT2C/HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2C",
         "CYP2D6", "CYP2E1", "CYP3A4", "CYP3A5", "CYP4F2", "COMT", "DPYD", "DRD2", "F2", "F5", "GRIK1", "GRIK4",
         "HLA*A", "HLA*B", "HTR2A", "IFNL4", "MC4R", "MTHFR", "NAT2", "NUDT15", "OPRM1", "SCL6A4", "SLCO1B1",
         "TPMT", "UGT1A1" "UGT1A4", "UGT2B15", "VKORC1"]

genes_psych = ["ABCB1", "ADRA2A", "5HT2C/HTR2C", "ANK3", "CYP1A2", "CYP2B6", "CYP2C19", "CYP2C9", "CYP2D6", "CYP2E1",
               "CYP3A4", "CYP3A5", "COMT", "DRD2", "GRIK1", "GRIK4", "HLA-A", "HLA-B", "HTR2A", "MC4R", "MTHFR", "NAT2",
               "OPRM1", "SCL6A4", "TPMT", "UGT1A1", "UGT1A4", "UGT2B15"]

variants_geno = ["rs3813929", "rs1045642", "rs2032583", "rs1800544", "rs10994336", "rs6265", "rs1006737", "rs4680",
                 "CYP1A2 (*1B, *1C, *1D, *1E, *1F, *1K, *11)", "CYP2B6 (*4, *5, *6)",
                 "CYP2C19 (*2, *3, *4, *5, *6, *7, *8, *9, *10, *17, *35)",
                 "CYP2C9 (*2, *3, *4, *5, *6, *8, *11, *13, *27)",
                 "CYP2D6 (*2, *3, *4, *5, *6, *7, *8, *9, *10, *11, *12, *14, *15, *17, *29, *41)", "CYP3A4 *22",
                 "CYP3A5 (*3, *6, *7)", "rs1799732", "rs2832407", "HLA-B*15:02", "HLA-B*15:13", "HLA-A*31:01/rs1061235",
                 "HLA-A*33", "rs7997012", "rs489693", "rs1801131", "rs1801133", "rs1799971", "rs25531", "rs63749047",
                 "rs1902023", "rs2011425"]

# 5HT2C rs3813929; ABCB1 C3435T rs1045642; ABCB1 rs2032583; ADRA2A rs1800544; ANK3 rs10994336; BDNF rs6265;
# CACNA1C rs1006737; COMT rs4680; CYP1A2 *1B, *1C, *1D, *1E, *1F, *1K y *11; CYP2B6 *4, *5, y *6; CYP2C19 *2, *3, *4,
# *5, *6, *7, *8, *9, *10, *17, y *35; CYP2C9 *2, *3, *4, *5, *6, *8, *11, *13, y *27; CYP2D6 *2, *3, *4, con
# eliminacion *5, duplicacion *6, *7, *8, *9, *10, *11, *12, *14, *15, *17, *29 y *41; CYP3A4 *22; CYP3A5 *3, *6, *7;
# DRD2 rs1799732; GRIK1 rs2832407; HLA-B*15:02 presencia con pruebas reflejas para presencia de HLA-B*15:13 para todas
# las muestras positivas y la secuencia de Sanger para todas las muestras doble positivo; HLA-A*31:01 rs1061235
# (indica la presencia de alelo HLA-A*31:01 y/o de alelos HLA-A*33); HTR2A rs7997012; MC4R rs489693; MTHFR rs1801131
# y rs1801133; OPRM1 rs1799971; SLC6A4 rs25531 y rs63749047; UGT2B15 rs1902023; y UGT1A4 rs2011425

variants_one = ["CYP1A2 (*1C, *1D, *1E, *1F, *1J, *1K, *1L, *1V, *1W)", "CYP2B6 (*4, *5, *6, *7, *9, *16, *18)",
                "CYP2C9 (*2, *3, *4, *5, *6, *8, *11)", "CYP2C19 (*2, *3, *4, *4B, *10, *17)", "CYP2D6 (*2, *2A, *3, "
                "*4, *4M, *4N, *5, *6, *6C, *7, *8, *9, *10, *11, *12, *13, *14, *15, *17, *18, *19, *20, *29, *31, "
                "*34, *35, *36, *39, 41, *42, *59, *63, *64, *68, *69, *70, *91, *109, *114)", "CYP3A4 (*1B, *22)",
                "CYP3A5 (*3, *6, *7)", "CYP4F2 *3", "DPYD (*2A, *13)", "SLCO1B1 (*5, *15, *17, *21)",
                "TPMT (*2, *3A, *3B, *3C, *4)", "UGT1A1 (*6, *28)"]

# CYP1A2 *1C, *1D, *1E, *1F, *1J, *1K, *1L, *1V, *1W
# CYP2B6 *4, *5, *6, *7, *9, *16, *18
# CYP2C9 *2, *3, *4, *5, *6, *8, *11
# CYP2C19 *2, *3, *4, *4B, *10, *17
# CYP2D6 *2, *2A, *3, *4, *4M, *4N, *5, *6, *6C, *7, *8, *9, *10, *11, *12, *13, *14, *15, *17, *18, *19, *20, *29, *31,
# *34, *35, *36, *39, 41, *42, *59, *63, *64, *68, *69, *70, *91, *109, *114
# CYP3A4 *1B, *22
# CYP3A5 *3, *6, *7
# CYP4F2 *3
# DPYD *2A, *13
# SLCO1B1 *5, *15, *17, *21
# TPMT *2, *3A, *3B, *3C, *4
# UGT1A1 *6, *28

variants_novo = []
# Las variantes de Novogenia completas deben ser pedidas por contacto a la empresa
