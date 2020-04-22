#compound library analysis script based on Alexander Varnek's Tutorials in Chemoinformatics CH 5
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.ML.Descriptors import MoleculeDescriptors

def moldescriptors(myfile):
    ms=[x for x in Chem.SDMolSupplier(myfile) if x is not None]
    ms_wr= open('descriptors.descr.tsv','w')
    nms=[x[0] for x in Descriptors._descList]
    calc=MoleculeDescriptors.MolecularDescriptorCalculator(nms)
    ms_wr.write("ID")
    for d in nms:
        ms_wr.write("\t")
        ms_wr.write(str(d))
    ms_wr.write("\n")
    for i in range(len(ms)):
        ms_wr.write(str(i))
        descrs= calc.CalcDescriptors(ms[i])
        for x in range(len(nms)):
            ms_wr.write("\t")
            ms_wr.write(str(descrs[x]))
    ms_wr.close()
