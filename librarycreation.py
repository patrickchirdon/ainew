from rdkit import Chem

def librarycreation(actives, inactives):
    suppl=Chem.SDMolSupplier(actives)
    myactives=[]
    for mol in suppl:
        if mol is None:
            continue
        mol.SetProp('ActiveTag', "1")
        myactives.append(mol)
    suppl2=Chem.SDMolSupplier(inactives)
    myinactives=[]
    for mol in suppl2:
        if mol is None:
            continue
        mol.SetProp('ActiveTag', "0")
        myinactives.append(mol)
    from rdkit.Chem import AllChem
    writer=Chem.SDWriter('newlibrary.sdf')
    writer.SetProps(['CID','ActiveTag'])
    for mol in myactives:
        AllChem.Compute2DCoords(mol)
        writer.write(mol)
    for mol in myinactives:
        AllChem.Compute2DCoords(mol)
        writer.write(mol)
    writer.close()
